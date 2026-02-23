"""Toast notification widget for account switch events."""
from __future__ import annotations

from textual.widgets import Static
from textual.containers import Container


class SwitchToast(Container):
    """Toast notification for account switching events."""

    DEFAULT_CSS = """
    SwitchToast {
        height: 3;
        width: 40;
        border: round $primary;
        background: $panel;
        align: center middle;
        offset: 0 -3;
    }

    .switch-toast-content {
        width: 1fr;
        color: $text;
        text-style: bold;
    }
    """

    def __init__(self, from_account: str, to_account: str, reason: str = "", **kwargs):
        super().__init__(**kwargs)
        self.from_account = from_account
        self.to_account = to_account
        self.reason = reason

    def compose(self):
        """Compose the toast message."""
        message = f"Switched: {self.from_account} → {self.to_account}"
        if self.reason:
            message += f"\n({self.reason})"
        yield Static(message, classes="switch-toast-content")

    def on_mount(self):
        """Auto-dismiss after 5 seconds."""
        self.app.set_timer(5.0, self.remove)
