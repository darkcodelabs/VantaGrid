"""Plugin loader and hook dispatch service."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from vantagrid.models.plugin import Plugin, PluginHook


class PluginService:
    """Manages plugin discovery, loading, and hook dispatch."""

    def discover(self, plugin_dir: Path) -> list[Plugin]:
        """Scan plugin directory for plugin.py files and create Plugin objects."""
        plugins = []

        if not plugin_dir.exists():
            return plugins

        for plugin_path in plugin_dir.iterdir():
            if not plugin_path.is_dir():
                continue

            plugin_py = plugin_path / "plugin.py"
            if plugin_py.exists():
                plugin = Plugin(
                    name=plugin_path.name,
                    description="",
                    version="1.0.0",
                    hooks=[],
                    enabled=True,
                    install_path=plugin_path,
                )
                plugins.append(plugin)

        return plugins

    def load(self, name: str, plugin_dir: Path) -> object:
        """Load a plugin module by name."""
        plugin_path = plugin_dir / name / "plugin.py"

        if not plugin_path.exists():
            raise ValueError(f"Plugin '{name}' not found")

        spec = importlib.util.spec_from_file_location(f"vantagrid_plugin_{name}", plugin_path)
        if spec is None or spec.loader is None:
            raise ValueError(f"Could not load plugin '{name}'")

        module = importlib.util.module_from_spec(spec)
        sys.modules[f"vantagrid_plugin_{name}"] = module
        spec.loader.exec_module(module)

        return module

    def dispatch(
        self, hook: PluginHook, plugin_dir: Path, **kwargs
    ) -> None:
        """Call a hook function on all plugins that have it."""
        plugins = self.discover(plugin_dir)

        for plugin in plugins:
            if not plugin.enabled or plugin.install_path is None:
                continue

            try:
                module = self.load(plugin.name, plugin_dir)

                # Look for hook handler function
                hook_name = hook.value
                if hasattr(module, hook_name):
                    handler = getattr(module, hook_name)
                    if callable(handler):
                        handler(**kwargs)
            except Exception:
                # Silently skip plugin errors during dispatch
                pass

    def get(self, name: str, plugin_dir: Path) -> Plugin | None:
        """Get a plugin by name."""
        for plugin in self.discover(plugin_dir):
            if plugin.name == name:
                return plugin
        return None
