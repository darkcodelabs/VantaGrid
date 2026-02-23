"""Smart account switching service with cooldown."""
from __future__ import annotations

from datetime import datetime, timedelta

from vantagrid.models.account import AccountUsage
from vantagrid.models.config import SwitchingConfig
from vantagrid.models.session import SessionSwitch


class SwitchService:
    """Manages smart switching logic with cooldown enforcement."""

    def __init__(self) -> None:
        self._history: list[SessionSwitch] = []
        self._last_switch_time: datetime | None = None

    def should_switch(self, usage: AccountUsage, config: SwitchingConfig) -> bool:
        """Check if usage exceeds auto-switch threshold."""
        if not config.enabled:
            return False
        return usage.weekly_all_pct >= config.auto_switch_threshold

    def should_warn(self, usage: AccountUsage, config: SwitchingConfig) -> bool:
        """Check if usage exceeds warning threshold."""
        if not config.enabled:
            return False
        return usage.weekly_all_pct >= config.warn_threshold

    def switch(self, from_name: str, to_name: str, reason: str) -> SessionSwitch:
        """Record a switch event and update cooldown."""
        switch = SessionSwitch(
            from_account=from_name,
            to_account=to_name,
            reason=reason,
        )
        self._history.append(switch)
        self._last_switch_time = datetime.now()
        return switch

    def can_switch(self, config: SwitchingConfig) -> bool:
        """Check if cooldown has expired."""
        if self._last_switch_time is None:
            return True

        cooldown_delta = timedelta(seconds=config.cooldown_seconds)
        return datetime.now() >= self._last_switch_time + cooldown_delta

    def get_history(self) -> list[SessionSwitch]:
        """Get switch history."""
        return self._history.copy()
