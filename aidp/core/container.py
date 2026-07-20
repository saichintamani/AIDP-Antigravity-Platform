"""Service container for dependency injection.

Register and retrieve singleton services throughout the application.
"""

class ServiceContainer:
    _services = {}

    @classmethod
    def register(cls, name: str, instance: object) -> None:
        """Register a service instance under a given name.

        If a service with the same name already exists, it will be overwritten.
        """
        cls._services[name] = instance

    @classmethod
    def get(cls, name: str) -> object:
        """Retrieve a registered service by name.

        Raises:
            KeyError: If the service is not registered.
        """
        if name not in cls._services:
            raise KeyError(f"Service '{name}' not registered.")
        return cls._services[name]
