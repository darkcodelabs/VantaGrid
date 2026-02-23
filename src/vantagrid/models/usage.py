from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field

class UsageSnapshot(BaseModel):
    account_name: str
    session_pct: float = Field(ge=0.0, le=1.0)
    weekly_pct: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.now)

class BurnRate(BaseModel):
    account_name: str
    pct_per_minute: float = Field(ge=0.0, default=0.0)
    estimated_depletion_minutes: float | None = None

class UsageHistory(BaseModel):
    snapshots: list[UsageSnapshot] = []
    max_snapshots: int = Field(default=100, ge=1)

    def add(self, snapshot: UsageSnapshot) -> None:
        self.snapshots.append(snapshot)
        if len(self.snapshots) > self.max_snapshots:
            self.snapshots = self.snapshots[-self.max_snapshots:]
