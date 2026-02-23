from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field

class AccountUsage(BaseModel):
    session_pct: float = Field(ge=0.0, le=1.0, default=0.0)
    weekly_all_pct: float = Field(ge=0.0, le=1.0, default=0.0)
    weekly_sonnet_pct: float = Field(ge=0.0, le=1.0, default=0.0)
    tokens_used: int = Field(ge=0, default=0)
    cost_usd: float = Field(ge=0.0, default=0.0)
    messages: int = Field(ge=0, default=0)
    reset_at: datetime | None = None
    updated_at: datetime = Field(default_factory=datetime.now)

class Account(BaseModel):
    name: str
    email: str = ""
    plan: Literal["free", "pro", "5x", "20x"] = "pro"
    config_dir: Path
    is_active: bool = False
    usage: AccountUsage | None = None
