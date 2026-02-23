"""Usage panel widget displaying usage progress bars for accounts."""
from __future__ import annotations

from textual.widgets import Static, ProgressBar
from textual.containers import Vertical
from textual.reactive import reactive


class UsagePanel(Vertical):
    """Panel showing usage progress bars and burn rates for each account."""

    DEFAULT_CSS = """
    UsagePanel {
        height: auto;
        border: 1 solid $primary;
        background: $panel;
        padding: 1;
    }

    .usage-row {
        height: 3;
        border: 1 solid $boost;
        padding: 1;
        margin: 0 0 1 0;
    }

    .usage-label {
        height: 1;
        width: 1fr;
        color: $text;
        text-style: bold;
    }

    .usage-bar {
        height: 1;
        width: 1fr;
    }

    .usage-percent {
        height: 1;
        color: $text-muted;
        width: 1fr;
    }

    ProgressBar {
        height: 1;
    }
    """

    is_visible = reactive(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_usage: dict[str, dict] = {}
        self._update_interval = None

    def compose(self):
        """Compose the usage panel."""
        # Will be populated dynamically
        yield Static("", id="usage-container")

    def on_mount(self):
        """Initialize the panel."""
        self._start_refresh()

    def on_unmount(self):
        """Stop refreshing when unmounted."""
        if self._update_interval:
            self.app.unset_interval(self._update_interval)

    def _start_refresh(self):
        """Start periodic refresh of usage data."""
        self._update_interval = self.app.set_interval(5.0, self._refresh)

    def _refresh(self):
        """Refresh usage display."""
        self._render_usage()

    def set_account_usage(self, account_name: str, usage_pct: float, burn_rate: str = ""):
        """Update usage for an account.

        Args:
            account_name: Account name
            usage_pct: Usage percentage (0.0-1.0)
            burn_rate: Burn rate string (e.g., "5% per minute")
        """
        self.account_usage[account_name] = {
            "usage_pct": usage_pct,
            "burn_rate": burn_rate,
        }
        self._render_usage()

    def _render_usage(self):
        """Render all usage rows."""
        self.query("Static").remove()
        if not self.account_usage:
            return

        for account, data in self.account_usage.items():
            usage_pct = data["usage_pct"]
            burn_rate = data.get("burn_rate", "")

            # Determine color based on usage level
            if usage_pct < 0.5:
                color = "green"
            elif usage_pct < 0.75:
                color = "yellow"
            elif usage_pct < 0.9:
                color = "yellow"
            else:
                color = "red"

            label = Static(f"{account}", classes="usage-label")
            percent_text = f"{usage_pct*100:.0f}% {burn_rate}"
            percent = Static(percent_text, classes="usage-percent")

            self.mount(label, percent)

    def toggle_visibility(self):
        """Toggle panel visibility."""
        self.is_visible = not self.is_visible
        self.display = self.is_visible
