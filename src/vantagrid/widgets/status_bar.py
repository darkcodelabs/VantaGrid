"""Status bar widget showing theme and usage information."""
from __future__ import annotations

from textual.widgets import Static
from textual.containers import Horizontal
from textual.reactive import reactive


class StatusBar(Horizontal):
    """Bottom status bar displaying theme, usage, and hotkey hints."""

    DEFAULT_CSS = """
    StatusBar {
        height: 1;
        background: $panel;
        border-top: solid $primary;
    }

    .status-left {
        width: 1fr;
        content-align: left middle;
    }

    .status-center {
        width: 2fr;
        content-align: center middle;
    }

    .status-right {
        width: 1fr;
        content-align: right middle;
    }

    .status-text {
        color: $text-muted;
    }

    .status-accent {
        color: $accent;
        text-style: bold;
    }
    """

    theme_name = reactive("synthwave")
    usage_text = reactive("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usage_data: dict[str, str] = {}

    def compose(self):
        """Compose the status bar sections."""
        yield Static("synthwave", classes="status-left status-text")
        yield Static("", classes="status-center status-text", id="status-usage")
        yield Static(
            "^S swap ^T theme ^B sidebar ^J bottom ^P palette ^K skills ^Q quit",
            classes="status-right status-text",
        )

    def on_mount(self):
        """Initialize status bar on mount."""
        self._update_usage()

    def watch_theme_name(self, name: str):
        """Update theme display."""
        left = self.query_one(".status-left", Static)
        left.update(name)

    def watch_usage_text(self, text: str):
        """Update usage display."""
        center = self.query_one("#status-usage", Static)
        center.update(text)

    def update_usage(self, usage_data: dict[str, str]):
        """Update usage information.

        Args:
            usage_data: Dictionary mapping account names to usage strings
        """
        self.usage_data = usage_data
        self._update_usage()

    def _update_usage(self):
        """Render usage text."""
        parts = []
        for account, usage in self.usage_data.items():
            parts.append(f"{account}: {usage}")
        self.usage_text = " | ".join(parts) if parts else ""

    def set_theme(self, theme_name: str):
        """Set the active theme name.

        Args:
            theme_name: Name of the theme
        """
        self.theme_name = theme_name
