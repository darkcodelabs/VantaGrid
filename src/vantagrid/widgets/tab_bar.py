"""Tab bar widget for managing multiple tabs."""
from __future__ import annotations

from textual.widgets import Static
from textual.containers import Horizontal
from textual.message import Message


class TabBar(Horizontal):
    """Horizontal tab bar for switching between panes."""

    class TabActivated(Message):
        """Posted when a tab is activated."""

        def __init__(self, tab_id: str):
            super().__init__()
            self.tab_id = tab_id

    class TabClosed(Message):
        """Posted when a tab is closed."""

        def __init__(self, tab_id: str):
            super().__init__()
            self.tab_id = tab_id

    DEFAULT_CSS = """
    TabBar {
        height: 3;
        background: $surface;
        border-bottom: solid $primary;
    }

    .tab {
        background: $panel;
        color: $text-muted;
        padding: 0 2;
        border-right: solid $panel;
    }

    .tab--active {
        background: $primary;
        color: $text;
        text-style: bold;
    }

    .tab--inactive:hover {
        background: $boost;
        color: $text;
    }
    """

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.tabs: dict[str, str] = {}
        self.active_tab: str | None = None

    def add_tab(self, tab_id: str, label: str) -> None:
        self.tabs[tab_id] = label
        if self.active_tab is None:
            self.active_tab = tab_id
        if self.is_mounted:
            is_active = tab_id == self.active_tab
            cls = "tab tab--active" if is_active else "tab tab--inactive"
            self.mount(Static(f" {label} ", classes=cls, name=tab_id))

    def remove_tab(self, tab_id: str) -> None:
        if tab_id in self.tabs:
            del self.tabs[tab_id]
            if self.active_tab == tab_id:
                self.active_tab = next(iter(self.tabs), None)
            for child in list(self.children):
                if child.name == tab_id:
                    child.remove()
            self.post_message(self.TabClosed(tab_id))

    def activate_tab(self, tab_id: str) -> None:
        if tab_id not in self.tabs:
            return
        self.active_tab = tab_id
        for child in self.children:
            if child.name == tab_id:
                child.set_classes("tab tab--active")
            else:
                child.set_classes("tab tab--inactive")
        self.post_message(self.TabActivated(tab_id))

    def on_click(self, event) -> None:
        """Handle tab click."""
        try:
            widget = self.screen.get_widget_at(event.screen_x, event.screen_y)
        except Exception:
            return
        if widget and hasattr(widget, "name") and widget.name in self.tabs:
            self.activate_tab(widget.name)
