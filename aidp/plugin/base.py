import abc
from typing import Any, Dict

class Plugin(abc.ABC):
    """Base class for all AIDP plugins.

    Subclasses should implement :meth:`initialize` to perform any startup
    actions and may expose a ``metadata`` dict describing the plugin.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Human‑readable name of the plugin."""
        ...

    @property
    def description(self) -> str:
        """Optional longer description. Defaults to empty string."""
        return ""

    @abc.abstractmethod
    def initialize(self, **kwargs: Any) -> None:
        """Hook called by the :class:`PluginRegistry` during startup.

        Implementers can use ``**kwargs`` to receive configuration or other
        runtime objects.
        """
        ...

    def metadata(self) -> Dict[str, Any]:
        """Return a dictionary of plugin metadata.

        The default implementation returns ``name`` and ``description`` but
        subclasses may extend it.
        """
        return {"name": self.name, "description": self.description}
