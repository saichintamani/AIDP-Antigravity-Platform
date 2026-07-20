from aidp.reasoning.dual_process import DualProcessOrchestrator
from aidp.reasoning.learning import LearningLoop, ProceduralMemory
from aidp.reasoning.pipeline import ReasoningPipeline
from aidp.reasoning.replay import ReasoningReplayEngine
from aidp.reasoning.telemetry import CognitiveTelemetryTracker


def test_pipeline_execution_and_telemetry() -> None:
    """Validates the 10-step lifecycle and captures cognitive telemetry."""
    pipeline = ReasoningPipeline()
    telemetry = CognitiveTelemetryTracker()

    observation = "Patient exhibits symptoms of X, and taking drug Y."

    # 1. Execute
    trace = pipeline.run(observation)

    # 2. Verify schema compliance
    assert trace["query"] == observation
    assert len(trace["steps"]) > 0
    assert trace["globalUncertainty"]["model"] > 0
    assert "reflection" in trace
    assert "memoryUpdates" in trace

    # 3. Telemetry capture
    record = telemetry.record_trace_execution(trace, latency_ms=150.0)
    assert record.average_hypotheses_per_step > 0
    assert record.reflection_iterations == 1
    assert record.memory_writes > 0


def test_dual_process() -> None:
    """Validates heuristic-based dispatch to System 1 vs System 2."""
    orchestrator = DualProcessOrchestrator(confidence_threshold=0.85)
    decision = orchestrator.evaluate_and_dispatch("Complex reasoning task")
    # Our mock currently hardcodes sys1_confidence = 0.70 < 0.85
    assert decision == "system_2"


def test_replay_engine() -> None:
    """Validates determinism scoring on replay."""
    pipeline = ReasoningPipeline()
    replay = ReasoningReplayEngine(reasoning_engine_fn=pipeline.run)

    historical = pipeline.run("Test query")
    score = replay.replay_and_compare(historical)

    # Pipeline is currently deterministic, should be 1.0
    assert score == 1.0


def test_learning_loop() -> None:
    """Validates pattern extraction from failing traces."""
    memory = ProceduralMemory()
    loop = LearningLoop(memory)

    failing_scorecard = {"hallucination_detected": True}
    trace = {}  # Mock

    extracted = loop.process_trace(trace, failing_scorecard)
    assert extracted
    assert len(memory.rules) == 1
    assert "ALWAYS verify" in memory.rules[0]
