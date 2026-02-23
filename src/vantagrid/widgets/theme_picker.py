"""Theme picker widget for selecting and previewing themes."""
from __future__ import annotations

from textual.widgets import Static
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import reactive


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
        border: solid $primary;
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

    themes_label: reactive[str] = reactive("")

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.themes: list[str] = []
        self.active_theme: str | None = None

    def compose(self):
        yield Static("THEMES", classes="theme-title")

    def set_themes(self, themes: list[str], active: str | None = None) -> None:
        self.themes = themes
        self.active_theme = active
        self._trigger_render()

    def set_active_theme(self, theme_name: str) -> None:
        self.active_theme = theme_name
        self._trigger_render()

    def _trigger_render(self) -> None:
        self.themes_label = f"{self.active_theme}|{'|'.join(self.themes)}"

    def watch_themes_label(self, _value: str) -> None:
        if not self.is_mounted:
            return
        # Remove old theme items (keep the title)
        for child in list(self.children):
            if "theme-item" in child.classes:
                child.remove()
        for theme in self.themes:
            is_active = theme == self.active_theme
            cls = "theme-item theme-item--active" if is_active else "theme-item"
            swatch = ">" if is_active else " "
            widget = Static(f"{swatch} {theme}", classes=cls, id=f"theme-{theme}")
            self.mount(widget)

    def on_click(self, event) -> None:
        """Handle theme selection via click."""
        try:
            widget = self.screen.get_widget_at(event.screen_x, event.screen_y)
        except Exception:
            return
        if widget and hasattr(widget, "id") and widget.id and widget.id.startswith("theme-"):
            theme_name = widget.id[6:]
            self.post_message(self.ThemeSelected(theme_name))
