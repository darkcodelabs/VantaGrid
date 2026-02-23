"""Status bar widget showing theme and usage information."""
from __future__ import annotations

from textual.widgets import Static
from textual.containers import Horizontal


class StatusBar(Horizontal):
    """Bottom status bar displaying theme, usage, and hotkey hints."""

    DEFAULT_CSS = """
    StatusBar {
        height: 1;
        background: $panel;
        color: $text;
    }

    #status-theme {
        width: auto;
        min-width: 14;
        padding: 0 1;
        color: $accent;
        text-style: bold;
    }

    #status-usage {
        width: 1fr;
        content-align: center middle;
        padding: 0 1;
    }

    #status-keys {
        width: auto;
        padding: 0 1;
        color: $text-muted;
    }
    """

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._theme = "synthwave"

    def compose(self):
        yield Static(f" {self._theme} ", id="status-theme")
        yield Static("", id="status-usage")
        yield Static("^S swap  ^T theme  ^B sidebar  ^J bottom  ^Q quit", id="status-keys")

    def set_theme(self, name: str) -> None:
        self._theme = name
        if self.is_mounted:
            self.query_one("#status-theme", Static).update(f" {name} ")

    def set_usage(self, text: str) -> None:
        if self.is_mounted:
            self.query_one("#status-usage", Static).update(text)
