from collections.abc import Callable
from typing import Any


class RayOrchestrator:
    """
    A lightweight wrapper to dispatch tasks to a Ray cluster.
    Degrades to local execution if RAY_ENABLED is false, allowing seamless local testing.
    """

    def __init__(self, enable_ray: bool = False) -> None:
        self.ray_enabled = enable_ray
        self._ray_initialized = False

        if self.ray_enabled:
            self._init_ray()

    def _init_ray(self) -> None:
        try:
            import ray

            if not ray.is_initialized():
                ray.init(ignore_reinit_error=True)
            self._ray_initialized = True
        except ImportError:
            print("Warning: ray package not found. Falling back to local execution.")
            self.ray_enabled = False

    def dispatch_task(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Dispatches a function to run either on the Ray cluster or locally.
        Returns a Future if Ray is enabled, else returns the direct result.
        """
        if self.ray_enabled and self._ray_initialized:
            import ray

            # Wrap function in ray remote if it's not already
            remote_func = ray.remote(func) if not hasattr(func, "remote") else func
            return remote_func.remote(*args, **kwargs)
        else:
            # Fallback to synchronous local execution
            return func(*args, **kwargs)

    def resolve_result(self, future_or_result: Any) -> Any:
        """
        Blocks and retrieves the result from Ray, or returns the result if local.
        """
        if self.ray_enabled and self._ray_initialized:
            import ray

            if isinstance(future_or_result, ray.ObjectRef):
                return ray.get(future_or_result)
        return future_or_result
