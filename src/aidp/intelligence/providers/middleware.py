import functools
import json
import re
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from aidp.intelligence.providers.base import RateLimitError
from aidp.intelligence.providers.capabilities import ReasoningTier
from aidp.intelligence.providers.routing import RoutingPolicy


@dataclass
class GatewayTrace:
    request_id: str
    timestamp: str
    provider_name: str
    prompt_version: str
    latency_ms: float
    retries: int
    cache_hit: bool
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    safety_violations: list[str]
    success: bool
    model_identifier: str = ""
    decoding_parameters: dict[str, Any] | None = field(default_factory=dict)
    routing_decision: str = ""


def with_retry(max_retries: int = 3, base_delay: float = 1.0) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Middleware decorator that applies exponential backoff for RateLimitErrors."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except RateLimitError as e:
                    if retries >= max_retries:
                        raise e
                    delay = base_delay * (2**retries)
                    time.sleep(delay)
                    retries += 1

        return wrapper

    return decorator


class InputSafetyLayer:
    """Sanitizes inputs to prevent prompt injection and malicious payloads."""
    
    @staticmethod
    def sanitize(prompt: str) -> None:
        # Heuristic check for prompt injection keywords
        blacklist = [
            "ignore previous instructions",
            "system prompt",
            "disregard all",
            "you are now a",
            "bypass safety",
            "override instructions"
        ]
        prompt_lower = prompt.lower()
        for term in blacklist:
            if term in prompt_lower:
                raise SecurityException(f"Prompt injection detected: banned term '{term}'")

class SecurityException(Exception):
    pass

class OutputSafetyLayer:
    """Validates epistemic invariants on the LLM output."""

    @staticmethod
    def validate(parsed_json: dict[str, Any] | BaseModel) -> list[str]:
        violations = []

        # If it's a pydantic model, convert to dict for these basic heuristic checks
        data = parsed_json.model_dump() if isinstance(parsed_json, BaseModel) else parsed_json

        # 1. Missing citations
        if "claims" in data:
            for claim in data["claims"]:
                if "citations" not in claim or not claim["citations"]:
                    violations.append(f"Claim missing citations: {claim.get('text', 'unknown')}")

        # 2. Confidence inconsistencies
        if "confidence" in data and "uncertainty" in data:
            conf = float(data["confidence"])
            unc = float(data["uncertainty"])
            if conf + unc > 1.01:
                violations.append(f"Confidence ({conf}) + Uncertainty ({unc}) exceeds 1.0")

        return violations


class IntelligenceGateway:
    """
    The production gateway for routing LLM requests.
    Enforces caching, token telemetry, output safety, and capability-based routing.
    """

    def __init__(self, routing_policy: RoutingPolicy, cache: dict[str, Any] | None = None) -> None:
        self.routing_policy = routing_policy
        self.cache = cache if cache is not None else {}
        self.traces: list[GatewayTrace] = []

    @with_retry(max_retries=3, base_delay=0.5)
    def query(
        self,
        prompt: str,
        schema_hint: Any | None = None,
        prompt_version: str = "v1.0",
        min_tier: ReasoningTier = ReasoningTier.BASIC,
    ) -> Any:
        """
        Executes an LLM query wrapped in the gateway protections.
        Dynamically routes to the best provider.
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())

        # 0. Input Safety Layer (Prompt Injection Defense)
        InputSafetyLayer.sanitize(prompt)

        provider = self.routing_policy.get_best_provider(
            min_reasoning_tier=min_tier, requires_structured_output=bool(schema_hint)
        )

        # 1. Semantic Caching
        cache_key = str(hash(f"{prompt}_{min_tier.name}"))
        if cache_key in self.cache:
            trace = self._record_trace(
                request_id,
                provider.__class__.__name__,
                prompt_version,
                start_time,
                0,
                True,
                0,
                0,
                0.0,
                [],
                True,
                getattr(provider, "model_name", "unknown"),
                {},
                f"Cached ({min_tier.name})",
            )
            self.traces.append(trace)
            # If a BaseModel is expected and cache gives dict, we convert it
            if isinstance(schema_hint, type) and issubclass(schema_hint, BaseModel):
                if isinstance(self.cache[cache_key], dict):
                    return schema_hint(**self.cache[cache_key])
            return self.cache[cache_key]

        # 2. Provider Execution with Structured Output & Safety Enforcement
        max_validation_retries = 2
        violations = []

        for attempt in range(max_validation_retries + 1):
            try:
                raw_response = provider.query(prompt, schema_hint) if hasattr(provider, "query") else provider.generate(prompt).raw_response

                # 3. Structured Output Validator
                parsed_json = self._extract_and_validate_json(raw_response, schema_hint)

                # 4. Output Safety Layer
                violations = OutputSafetyLayer.validate(parsed_json)
                if violations:
                    raise ValueError(f"Safety violations: {violations}")

                # Cache and return
                self.cache[cache_key] = parsed_json

                # Record success trace
                trace = self._record_trace(
                    request_id,
                    provider.__class__.__name__,
                    prompt_version,
                    start_time,
                    attempt,
                    False,
                    len(prompt.split()),
                    len(str(raw_response).split()),
                    0.0,
                    [],
                    True,
                    getattr(provider, "model_name", "unknown"),
                    getattr(provider, "default_params", {}),
                    min_tier.name,
                )
                self.traces.append(trace)
                return parsed_json

            except ValueError as e:
                if attempt < max_validation_retries:
                    prompt += (
                        f"\n\nERROR IN PREVIOUS OUTPUT: {str(e)}. Please correct the response."
                    )
                else:
                    # Record failure trace
                    trace = self._record_trace(
                        request_id,
                        provider.__class__.__name__,
                        prompt_version,
                        start_time,
                        attempt,
                        False,
                        len(prompt.split()),
                        0,
                        0.0,
                        violations,
                        False,
                        getattr(provider, "model_name", "unknown"),
                        getattr(provider, "default_params", {}),
                        min_tier.name,
                    )
                    self.traces.append(trace)
                    raise RuntimeError(
                        f"LLM failed validation after {max_validation_retries} retries. Last error: {str(e)}"
                    )

        # This should never be reached, but satisfies mypy
        raise RuntimeError("Unexpected: validation loop exited without return or raise")

    def _extract_and_validate_json(self, response: Any, schema_hint: Any | None = None) -> Any:
        """Intercepts raw LLM strings, strips markdown, parses JSON, and validates schema keys."""
        if isinstance(response, BaseModel):
            return response
            
        if isinstance(response, dict):
            parsed = response
        else:
            clean_str = str(response)
            match = re.search(r"```(?:json)?(.*?)```", clean_str, re.DOTALL)
            if match:
                clean_str = match.group(1).strip()

            try:
                parsed = json.loads(clean_str)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON: {str(e)}\nRaw output: {response}")

        # If schema_hint is a Pydantic class, validate into the model!
        if isinstance(schema_hint, type) and issubclass(schema_hint, BaseModel):
            try:
                # Convert the raw dict into the strongly typed Pydantic model
                return schema_hint(**parsed)
            except Exception as e:
                raise ValueError(f"Pydantic Validation Error: {str(e)}")

        if isinstance(schema_hint, dict):
            missing_keys = [k for k in schema_hint if k not in parsed]
            if missing_keys:
                for k in missing_keys:
                    parsed[k] = schema_hint[k]

        return parsed

    def _record_trace(
        self,
        req_id: str,
        provider: str,
        prompt_v: str,
        start_time: float,
        retries: int,
        cache_hit: bool,
        in_tokens: int,
        out_tokens: int,
        cost: float,
        violations: list[str],
        success: bool,
        model_id: str = "",
        decoding: dict[str, Any] | None = None,
        routing: str = "",
    ) -> GatewayTrace:
        return GatewayTrace(
            request_id=req_id,
            timestamp=datetime.utcnow().isoformat(),
            provider_name=provider,
            prompt_version=prompt_v,
            latency_ms=(time.time() - start_time) * 1000,
            retries=retries,
            cache_hit=cache_hit,
            input_tokens=in_tokens,
            output_tokens=out_tokens,
            estimated_cost_usd=cost,
            safety_violations=violations,
            success=success,
            model_identifier=model_id,
            decoding_parameters=decoding or {},
            routing_decision=routing,
        )
