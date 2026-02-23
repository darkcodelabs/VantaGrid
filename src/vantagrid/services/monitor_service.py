"""Async usage monitoring service."""
from __future__ import annotations

import asyncio
from datetime import datetime

from vantagrid.models.account import Account, AccountUsage
from vantagrid.models.usage import BurnRate, UsageHistory, UsageSnapshot


class MonitorService:
    """Async service for monitoring account usage with polling."""

    def __init__(self) -> None:
        self._task: asyncio.Task | None = None
        self._snapshots: dict[str, UsageSnapshot] = {}
        self._histories: dict[str, UsageHistory] = {}
        self._interval: float = 60.0

    async def start(self, accounts: list[Account], interval: float = 60.0) -> None:
        """Start async polling loop for account usage."""
        self._interval = interval
        self._task = asyncio.create_task(self._poll_loop(accounts))

    async def stop(self) -> None:
        """Stop the polling task."""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    def get_snapshot(self, account_name: str) -> UsageSnapshot | None:
        """Get the latest usage snapshot for an account."""
        return self._snapshots.get(account_name)

    def get_burn_rate(self, account_name: str) -> BurnRate:
        """Calculate burn rate based on usage history."""
        history = self._histories.get(account_name)
        if not history or len(history.snapshots) < 2:
            return BurnRate(account_name=account_name, pct_per_minute=0.0)

        snapshots = history.snapshots
        latest = snapshots[-1]
        prev = snapshots[-2]

        time_delta = (latest.timestamp - prev.timestamp).total_seconds()
        if time_delta <= 0:
            return BurnRate(account_name=account_name, pct_per_minute=0.0)

        pct_delta = latest.weekly_pct - prev.weekly_pct
        pct_per_minute = pct_delta / (time_delta / 60.0)

        estimated_minutes = None
        if pct_per_minute > 0:
            remaining = 1.0 - latest.weekly_pct
            estimated_minutes = remaining / pct_per_minute

        return BurnRate(
            account_name=account_name,
            pct_per_minute=max(0.0, pct_per_minute),
            estimated_depletion_minutes=estimated_minutes,
        )

    def get_history(self, account_name: str) -> UsageHistory:
        """Get usage history for an account."""
        return self._histories.get(account_name, UsageHistory())

    async def _poll_loop(self, accounts: list[Account]) -> None:
        """Internal polling loop."""
        while True:
            try:
                for account in accounts:
                    if account.usage:
                        snapshot = UsageSnapshot(
                            account_name=account.name,
                            session_pct=account.usage.session_pct,
                            weekly_pct=account.usage.weekly_all_pct,
                        )
                        self._snapshots[account.name] = snapshot

                        # Add to history
                        if account.name not in self._histories:
                            self._histories[account.name] = UsageHistory()
                        self._histories[account.name].add(snapshot)

                await asyncio.sleep(self._interval)
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(self._interval)
