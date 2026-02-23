from __future__ import annotations
from datetime import datetime
from enum import Enum
from pathlib import Path
from pydantic import BaseModel, Field

class SessionState(str, Enum):
    STARTING = "starting"
    RUNNING = "running"
    IDLE = "idle"
    STOPPED = "stopped"

class Session(BaseModel):
    id: str
    account_name: str
    state: SessionState = SessionState.STARTING
    pid: int | None = None
    started_at: datetime = Field(default_factory=datetime.now)
    working_dir: Path = Field(default_factory=Path.cwd)

class SessionSwitch(BaseModel):
    from_account: str
    to_account: str
    reason: str
    switched_at: datetime = Field(default_factory=datetime.now)
