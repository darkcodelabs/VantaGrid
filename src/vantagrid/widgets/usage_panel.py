"""Usage panel widget displaying usage information for accounts."""
from __future__ import annotations

from textual.widgets import Static


class UsagePanel(Static):
    """Panel showing usage bars and info for each account."""

    DEFAULT_CSS = """
    UsagePanel {
        height: 1fr;
        padding: 0 1;
        color: $text;
    }
    """

    def __init__(self, **kwargs: object) -> None:
        super().__init__("", markup=True, **kwargs)
        self._accounts: dict[str, float] = {}

    def on_mount(self) -> None:
        self._refresh_display()

    def set_account_usage(self, account_name: str, usage_pct: float, burn_rate: str = "") -> None:
        self._accounts[account_name] = usage_pct
        self._refresh_display()

    def _refresh_display(self) -> None:
        if not self.is_mounted:
            return

        if not self._accounts:
            self.update("[bold]USAGE[/]\n No usage data")
            return

        lines = ["[bold]USAGE[/]"]
        for name, pct in self._accounts.items():
            pct_int = int(pct * 100)
            filled = int(pct * 20)
            empty = 20 - filled

            if pct < 0.5:
                color = "green"
            elif pct < 0.75:
                color = "yellow"
            elif pct < 0.9:
                color = "dark_orange"
            else:
                color = "red"

            bar = f"[{color}]{'█' * filled}[/][dim]{'░' * empty}[/]"
            lines.append(f" {name:<12} {bar} {pct_int:>3}%")

        self.update("\n".join(lines))
