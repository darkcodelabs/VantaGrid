"""Theme picker widget for selecting and previewing themes."""
from __future__ import annotations

from textual.widgets import Static
from textual.containers import Vertical
from textual.message import Message


class ThemePicker(Vertical):
    """Sidebar section for browsing and selecting themes."""

    class ThemeSelected(Message):
        """Posted when a theme is selected."""

        def __init__(self, theme_name: str):
            super().__init__()
            self.theme_name = theme_name

    DEFAULT_CSS = """
    ThemePicker {
        height: auto;
        border: 1 solid $primary;
        overflow: auto;
    }

    .theme-title {
        height: 1;
        background: $boost;
        color: $text;
        text-style: bold;
        padding: 0 1;
    }

    .theme-item {
        height: 1;
        padding: 0 1;
        margin: 0 0 1 0;
        color: $text-muted;
    }

    .theme-item--active {
        background: $accent;
        color: $panel;
        text-style: bold;
    }

    .theme-item:hover {
        background: $boost;
        color: $text;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.themes: list[str] = []
        self.active_theme: str | None = None

    def compose(self):
        """Compose the theme picker."""
        yield Static("THEMES", classes="theme-title")

    def set_themes(self, themes: list[str], active: str | None = None):
        """Set the list of available themes.

        Args:
            themes: List of theme names
            active: Currently active theme name
        """
        self.themes = themes
        self.active_theme = active
        self._render_themes()

    def set_active_theme(self, theme_name: str):
        """Mark a theme as active.

        Args:
            theme_name: Name of the theme to activate
        """
        self.active_theme = theme_name
        self._render_themes()

    def _render_themes(self):
        """Re-render the theme list."""
        self.query("Static").remove()
        self.mount(Static("THEMES", classes="theme-title"))

        for theme in self.themes:
            is_active = theme == self.active_theme
            class_name = "theme-item theme-item--active" if is_active else "theme-item"
            swatch = "◼" if is_active else "◻"
            label = f"{swatch} {theme}"
            widget = Static(label, classes=class_name, id=f"theme-{theme}")
            self.mount(widget)

    def on_static_pressed(self, event: Static.Pressed) -> None:
        """Handle theme selection."""
        widget = event.static
        if widget.id and widget.id.startswith("theme-"):
            theme_name = widget.id[6:]
            self.post_message(self.ThemeSelected(theme_name))
