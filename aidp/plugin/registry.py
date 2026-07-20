import importlib.metadata
import logging
from typing import Dict, List

from .base import Plugin

_logger = logging.getLogger(__name__)

class PluginRegistry:
    """Discover and instantiate AIDP plugins via entry‑points.

    Plugins should be registered under the ``aidp_plugins`` entry‑point group
    and expose a subclass of :class:`aidp.plugin.base.Plugin`.
    """

    def __init__(self) -> None:
        self._plugins: Dict[str, Plugin] = {}
        self._load_plugins()

    def _load_plugins(self) -> None:
        """Load all entry‑point plugins and instantiate them.

        Errors are logged but do not stop the loading process – a faulty plugin
        should not break the whole platform.
        """
        for ep in importlib.metadata.entry_points().select(group="aidp_plugins"):
            try:
                plugin_cls = ep.load()
                if not issubclass(plugin_cls, Plugin):
                    _logger.warning("Entry point %s does not inherit Plugin; skipping", ep.name)
                    continue
                instance = plugin_cls()
                self._plugins[instance.name] = instance
                _logger.info("Loaded AIDP plugin %s (%s)", instance.name, ep.name)
            except Exception as exc:  # pragma: no cover – defensive
                _logger.exception("Failed to load AIDP plugin %s: %s", ep.name, exc)

    def get(self, name: str) -> Plugin:
        """Return a plugin by its *human readable* name.

        Raises ``KeyError`` if the plugin is not registered.
        """
        return self._plugins[name]

    def all(self) -> List[Plugin]:
        """Return a list of all loaded plugin instances."""
        return list(self._plugins.values())
