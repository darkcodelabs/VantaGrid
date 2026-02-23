"""Plugin browser widget for managing plugins."""
from __future__ import annotations

from textual.widgets import Static, Button, Switch
from textual.containers import Vertical, Horizontal
from textual.message import Message


class PluginBrowser(Vertical):
    """Panel for browsing and managing plugins."""

    class PluginToggled(Message):
        """Posted when a plugin is toggled."""

        def __init__(self, plugin_name: str, enabled: bool):
            super().__init__()
            self.plugin_name = plugin_name
            self.enabled = enabled

    DEFAULT_CSS = """
    PluginBrowser {
        height: 1fr;
        border: 1 solid $primary;
        overflow: auto;
    }

    .plugin-title {
        height: 1;
        background: $boost;
        color: $text;
        text-style: bold;
        padding: 0 1;
    }

    .plugin-item {
        height: 4;
        border: 1 solid $panel;
        padding: 1;
        margin: 0 0 1 0;
    }

    .plugin-name {
        height: 1;
        color: $accent;
        text-style: bold;
    }

    .plugin-description {
        height: 1;
        color: $text-muted;
        width: 1fr;
    }

    .plugin-hooks {
        height: 1;
        color: $text-muted;
        width: 1fr;
    }

    .plugin-toggle {
        height: 1;
        width: auto;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plugins: dict[str, dict] = {}  # name -> {desc, hooks, enabled}

    def compose(self):
        """Compose the plugin browser."""
        yield Static("PLUGINS", classes="plugin-title")
        yield Static("", id="plugins-container")

    def add_plugin(
        self, name: str, description: str = "", hooks: list[str] | None = None, enabled: bool = False
    ):
        """Add a plugin to the list.

        Args:
            name: Plugin name
            description: Plugin description
            hooks: List of hook names
            enabled: Whether plugin is enabled
        """
        self.plugins[name] = {
            "description": description,
            "hooks": hooks or [],
            "enabled": enabled,
        }
        self._render_plugins()

    def _render_plugins(self):
        """Re-render the plugin list."""
        self.query("Horizontal").remove()

        for name, info in self.plugins.items():
            desc = info["description"]
            hooks = ", ".join(info["hooks"]) if info["hooks"] else "No hooks"
            enabled = info["enabled"]

            row = Vertical(
                Horizontal(
                    Static(name, classes="plugin-name"),
                    Switch(value=enabled, id=f"plugin-toggle-{name}"),
                    classes="plugin-toggle",
                ),
                Static(desc, classes="plugin-description"),
                Static(f"Hooks: {hooks}", classes="plugin-hooks"),
                classes="plugin-item",
            )
            self.mount(row)

    def on_switch_changed(self, event: Switch.Changed) -> None:
        """Handle toggle changes."""
        switch = event.control
        if switch.id and switch.id.startswith("plugin-toggle-"):
            plugin_name = switch.id[14:]
            self.plugins[plugin_name]["enabled"] = event.value
            self.post_message(self.PluginToggled(plugin_name, event.value))
