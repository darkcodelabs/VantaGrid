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
        border: round $primary;
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

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.themes: list[str] = []
        self.active_theme: str | None = None

    def compose(self):
        yield Static("THEMES", classes="theme-title")

    def set_themes(self, themes: list[str], active: str | None = None) -> None:
        self.themes = themes
        self.active_theme = active
        if self.is_mounted:
            self._mount_theme_items()

    def set_active_theme(self, theme_name: str) -> None:
        self.active_theme = theme_name
        if self.is_mounted:
            self._update_active_highlight()

    def _mount_theme_items(self) -> None:
        """Mount theme items (called once on initial population)."""
        for theme in self.themes:
            is_active = theme == self.active_theme
            cls = "theme-item theme-item--active" if is_active else "theme-item"
            swatch = ">" if is_active else " "
            self.mount(Static(f"{swatch} {theme}", classes=cls, name=f"t-{theme}"))

    def _update_active_highlight(self) -> None:
        """Update active theme highlight in-place (no remove/remount)."""
        for child in self.children:
            if not hasattr(child, "name") or not child.name or not child.name.startswith("t-"):
                continue
            theme = child.name[2:]
            is_active = theme == self.active_theme
            swatch = ">" if is_active else " "
            child.update(f"{swatch} {theme}")
            if is_active:
                child.set_classes("theme-item theme-item--active")
            else:
                child.set_classes("theme-item")

    def on_click(self, event) -> None:
        """Handle theme selection via click."""
        try:
            widget = self.screen.get_widget_at(event.screen_x, event.screen_y)
        except Exception:
            return
        if widget and hasattr(widget, "name") and widget.name and widget.name.startswith("t-"):
            theme_name = widget.name[2:]
            self.post_message(self.ThemeSelected(theme_name))
