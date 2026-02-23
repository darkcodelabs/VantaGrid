"""Tab bar widget for managing multiple tabs."""
from __future__ import annotations

from textual.widgets import Static
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import reactive


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

    tab_labels: reactive[str] = reactive("")

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.tabs: dict[str, str] = {}
        self.active_tab: str | None = None

    def add_tab(self, tab_id: str, label: str) -> None:
        self.tabs[tab_id] = label
        if self.active_tab is None:
            self.active_tab = tab_id
        self._update_labels()

    def remove_tab(self, tab_id: str) -> None:
        if tab_id in self.tabs:
            del self.tabs[tab_id]
            if self.active_tab == tab_id:
                self.active_tab = next(iter(self.tabs), None)
            self._update_labels()
            self.post_message(self.TabClosed(tab_id))

    def activate_tab(self, tab_id: str) -> None:
        if tab_id in self.tabs:
            self.active_tab = tab_id
            self._update_labels()
            self.post_message(self.TabActivated(tab_id))

    def _update_labels(self) -> None:
        """Update the reactive label string to trigger re-render."""
        parts = []
        for tab_id, label in self.tabs.items():
            marker = ">" if tab_id == self.active_tab else " "
            parts.append(f"{marker}{tab_id}:{label}")
        self.tab_labels = "|".join(parts)

    def compose(self):
        for tab_id, label in self.tabs.items():
            is_active = tab_id == self.active_tab
            cls = "tab tab--active" if is_active else "tab tab--inactive"
            yield Static(f" {label} ", classes=cls, id=f"tab-{tab_id}")

    def watch_tab_labels(self, _value: str) -> None:
        """Re-render tabs when labels change."""
        if not self.is_mounted:
            return
        # Remove existing tab widgets and add new ones
        for child in list(self.children):
            child.remove()
        for tab_id, label in self.tabs.items():
            is_active = tab_id == self.active_tab
            cls = "tab tab--active" if is_active else "tab tab--inactive"
            widget = Static(f" {label} ", classes=cls, id=f"tab-{tab_id}")
            self.mount(widget)

    def on_click(self, event) -> None:
        """Handle tab click."""
        try:
            widget = self.screen.get_widget_at(event.screen_x, event.screen_y)
        except Exception:
            return
        if widget and hasattr(widget, "id") and widget.id and widget.id.startswith("tab-"):
            tab_id = widget.id[4:]
            self.activate_tab(tab_id)
