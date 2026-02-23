"""Test SwitchService."""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from vantagrid.models.account import AccountUsage
from vantagrid.models.config import SwitchingConfig
from vantagrid.services.switch_service import SwitchService


class TestSwitchService:
    """Test SwitchService."""

    def test_should_switch_when_above_threshold(self) -> None:
        """Test should_switch returns True when usage exceeds threshold."""
        service = SwitchService()
        usage = AccountUsage(weekly_all_pct=0.95)
        config = SwitchingConfig(enabled=True, auto_switch_threshold=0.90)

        assert service.should_switch(usage, config) is True

    def test_should_switch_when_at_threshold(self) -> None:
        """Test should_switch returns True when usage equals threshold."""
        service = SwitchService()
        usage = AccountUsage(weekly_all_pct=0.90)
        config = SwitchingConfig(enabled=True, auto_switch_threshold=0.90)

        assert service.should_switch(usage, config) is True

    def test_should_switch_when_below_threshold(self) -> None:
        """Test should_switch returns False when below threshold."""
        service = SwitchService()
        usage = AccountUsage(weekly_all_pct=0.85)
        config = SwitchingConfig(enabled=True, auto_switch_threshold=0.90)

        assert service.should_switch(usage, config) is False

    def test_should_switch_disabled(self) -> None:
        """Test should_switch returns False when switching disabled."""
        service = SwitchService()
        usage = AccountUsage(weekly_all_pct=0.95)
        config = SwitchingConfig(enabled=False, auto_switch_threshold=0.90)

        assert service.should_switch(usage, config) is False

    def test_should_warn_when_above_threshold(self) -> None:
        """Test should_warn returns True when usage exceeds threshold."""
        service = SwitchService()
        usage = AccountUsage(weekly_all_pct=0.80)
        config = SwitchingConfig(enabled=True, warn_threshold=0.75)

        assert service.should_warn(usage, config) is True

    def test_should_warn_when_at_threshold(self) -> None:
        """Test should_warn returns True when usage equals threshold."""
        service = SwitchService()
        usage = AccountUsage(weekly_all_pct=0.75)
        config = SwitchingConfig(enabled=True, warn_threshold=0.75)

        assert service.should_warn(usage, config) is True

    def test_should_warn_when_below_threshold(self) -> None:
        """Test should_warn returns False when below threshold."""
        service = SwitchService()
        usage = AccountUsage(weekly_all_pct=0.70)
        config = SwitchingConfig(enabled=True, warn_threshold=0.75)

        assert service.should_warn(usage, config) is False

    def test_should_warn_disabled(self) -> None:
        """Test should_warn returns False when switching disabled."""
        service = SwitchService()
        usage = AccountUsage(weekly_all_pct=0.80)
        config = SwitchingConfig(enabled=False, warn_threshold=0.75)

        assert service.should_warn(usage, config) is False

    def test_switch_records_event(self) -> None:
        """Test switch records SessionSwitch."""
        service = SwitchService()
        switch = service.switch("acc1", "acc2", "High usage")

        assert switch.from_account == "acc1"
        assert switch.to_account == "acc2"
        assert switch.reason == "High usage"
        assert isinstance(switch.switched_at, datetime)

    def test_switch_updates_last_time(self) -> None:
        """Test switch updates last_switch_time."""
        service = SwitchService()
        assert service._last_switch_time is None

        service.switch("acc1", "acc2", "High usage")
        assert service._last_switch_time is not None

    def test_can_switch_initially_true(self) -> None:
        """Test can_switch returns True initially."""
        service = SwitchService()
        config = SwitchingConfig(cooldown_seconds=30)

        assert service.can_switch(config) is True

    def test_can_switch_before_cooldown_expires(self) -> None:
        """Test can_switch returns False before cooldown expires."""
        service = SwitchService()
        config = SwitchingConfig(cooldown_seconds=30)

        service.switch("acc1", "acc2", "Test")
        assert service.can_switch(config) is False

    def test_can_switch_after_cooldown_expires(self) -> None:
        """Test can_switch returns True after cooldown expires."""
        service = SwitchService()
        config = SwitchingConfig(cooldown_seconds=1)

        service.switch("acc1", "acc2", "Test")
        assert service.can_switch(config) is False

        import time

        time.sleep(1.1)
        assert service.can_switch(config) is True

    def test_get_history(self) -> None:
        """Test get_history returns switch history."""
        service = SwitchService()
        service.switch("acc1", "acc2", "Reason 1")
        service.switch("acc2", "acc3", "Reason 2")

        history = service.get_history()
        assert len(history) == 2
        assert history[0].from_account == "acc1"
        assert history[1].from_account == "acc2"

    def test_get_history_returns_copy(self) -> None:
        """Test get_history returns a copy (not reference)."""
        service = SwitchService()
        service.switch("acc1", "acc2", "Test")

        history1 = service.get_history()
        history2 = service.get_history()

        assert history1 is not history2
        assert history1 == history2
