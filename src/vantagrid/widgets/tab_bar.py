"""Tab bar widget for managing multiple tabs."""
from __future__ import annotations

from dataclasses import dataclass
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
        height: 1;
        background: $surface;
        border-bottom: 1 solid $primary;
    }

    .tab {
        background: $panel;
        color: $text-muted;
        padding: 0 2;
        text-style: normal;
        border-right: 1 solid $panel;
    }

    .tab--active {
        background: $primary;
        color: $text;
        text-style: bold;
        border-bottom: 1 double $accent;
    }

    .tab--inactive:hover {
        background: $boost;
        color: $text;
    }

    .tab-close {
        color: $text-muted;
        margin-left: 1;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tabs: dict[str, str] = {}  # id -> label
        self.active_tab: str | None = None

    def add_tab(self, tab_id: str, label: str):
        """Add a new tab.

        Args:
            tab_id: Unique identifier for the tab
            label: Display label for the tab
        """
        self.tabs[tab_id] = label
        self._render_tabs()
        if not self.active_tab:
            self.activate_tab(tab_id)

    def remove_tab(self, tab_id: str):
        """Remove a tab by ID.

        Args:
            tab_id: Tab identifier to remove
        """
        if tab_id in self.tabs:
            del self.tabs[tab_id]
            if self.active_tab == tab_id:
                self.active_tab = next(iter(self.tabs), None)
            self._render_tabs()
            self.post_message(self.TabClosed(tab_id))

    def activate_tab(self, tab_id: str):
        """Activate a tab by ID.

        Args:
            tab_id: Tab identifier to activate
        """
        if tab_id in self.tabs:
            self.active_tab = tab_id
            self._render_tabs()
            self.post_message(self.TabActivated(tab_id))

    def _render_tabs(self):
        """Re-render the tab bar."""
        self.query("Static").remove()
        for tab_id, label in self.tabs.items():
            is_active = tab_id == self.active_tab
            class_name = "tab tab--active" if is_active else "tab tab--inactive"
            tab_widget = Static(f"{label} ✕", classes=class_name, id=f"tab-{tab_id}")
            self.mount(tab_widget)
            if is_active:
                tab_widget.focus()

    def on_static_pressed(self, event: Static.Pressed) -> None:
        """Handle tab click."""
        widget = event.static
        if widget.id and widget.id.startswith("tab-"):
            tab_id = widget.id[4:]
            self.activate_tab(tab_id)
