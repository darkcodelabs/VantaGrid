"""Test MonitorService."""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from vantagrid.models.account import Account, AccountUsage
from vantagrid.models.usage import UsageSnapshot
from vantagrid.services.monitor_service import MonitorService


class TestMonitorService:
    """Test MonitorService."""

    def test_get_snapshot_returns_none_initially(self) -> None:
        """Test get_snapshot returns None when no data."""
        service = MonitorService()
        snapshot = service.get_snapshot("test")
        assert snapshot is None

    def test_get_burn_rate_returns_defaults(self) -> None:
        """Test get_burn_rate returns BurnRate with defaults."""
        service = MonitorService()
        burn_rate = service.get_burn_rate("test")

        assert burn_rate.account_name == "test"
        assert burn_rate.pct_per_minute == 0.0
        assert burn_rate.estimated_depletion_minutes is None

    def test_get_history_returns_empty(self) -> None:
        """Test get_history returns empty UsageHistory."""
        service = MonitorService()
        history = service.get_history("test")

        assert history.snapshots == []
        assert history.max_snapshots == 100

    @pytest.mark.asyncio
    async def test_start_and_stop(self) -> None:
        """Test start and stop lifecycle."""
        service = MonitorService()
        accounts = [Account(name="test", config_dir="/tmp/test")]

        await service.start(accounts, interval=0.1)
        assert service._task is not None

        await service.stop()
        assert service._task is None

    @pytest.mark.asyncio
    async def test_poll_loop_captures_snapshots(self) -> None:
        """Test poll_loop captures snapshots from accounts."""
        service = MonitorService()
        usage = AccountUsage(session_pct=0.5, weekly_all_pct=0.6)
        accounts = [Account(name="test", config_dir="/tmp/test", usage=usage)]

        await service.start(accounts, interval=0.05)
        await __import__("asyncio").sleep(0.1)
        await service.stop()

        snapshot = service.get_snapshot("test")
        assert snapshot is not None
        assert snapshot.account_name == "test"
        assert snapshot.session_pct == 0.5
        assert snapshot.weekly_pct == 0.6

    @pytest.mark.asyncio
    async def test_burn_rate_calculation(self) -> None:
        """Test burn rate calculation from history."""
        service = MonitorService()

        now = datetime.now()
        snap1 = UsageSnapshot(
            account_name="test",
            session_pct=0.5,
            weekly_pct=0.5,
            timestamp=now,
        )
        snap2 = UsageSnapshot(
            account_name="test",
            session_pct=0.5,
            weekly_pct=0.6,
            timestamp=now + timedelta(minutes=10),
        )

        service._histories["test"] = service.get_history("test")
        service._histories["test"].add(snap1)
        service._histories["test"].add(snap2)

        burn_rate = service.get_burn_rate("test")

        assert burn_rate.account_name == "test"
        assert burn_rate.pct_per_minute > 0
        assert burn_rate.estimated_depletion_minutes is not None

    @pytest.mark.asyncio
    async def test_burn_rate_with_single_snapshot(self) -> None:
        """Test burn rate with less than 2 snapshots."""
        service = MonitorService()

        snap1 = UsageSnapshot(
            account_name="test",
            session_pct=0.5,
            weekly_pct=0.5,
        )

        service._histories["test"] = service.get_history("test")
        service._histories["test"].add(snap1)

        burn_rate = service.get_burn_rate("test")

        assert burn_rate.pct_per_minute == 0.0
        assert burn_rate.estimated_depletion_minutes is None

    @pytest.mark.asyncio
    async def test_history_accumulates_snapshots(self) -> None:
        """Test history accumulates snapshots."""
        service = MonitorService()

        snap1 = UsageSnapshot(
            account_name="test",
            session_pct=0.5,
            weekly_pct=0.5,
        )
        snap2 = UsageSnapshot(
            account_name="test",
            session_pct=0.5,
            weekly_pct=0.6,
        )

        service._histories["test"] = service.get_history("test")
        service._histories["test"].add(snap1)
        service._histories["test"].add(snap2)

        history = service.get_history("test")
        assert len(history.snapshots) == 2
