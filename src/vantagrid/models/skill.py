from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Literal
from pydantic import BaseModel

class Skill(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    source: Literal["builtin", "community", "custom"] = "builtin"
    installed: bool = False
    install_path: Path | None = None
    tags: list[str] = []

class SkillRegistry(BaseModel):
    skills: list[Skill] = []
    last_fetched: datetime | None = None
    registry_url: str | None = None
