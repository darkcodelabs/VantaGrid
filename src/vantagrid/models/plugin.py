from __future__ import annotations
from enum import Enum
from pathlib import Path
from pydantic import BaseModel

class PluginHook(str, Enum):
    ON_SESSION_START = "on_session_start"
    ON_SWITCH = "on_switch"
    ON_USAGE_UPDATE = "on_usage_update"
    ON_THEME_CHANGE = "on_theme_change"

class Plugin(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    hooks: list[PluginHook] = []
    enabled: bool = True
    install_path: Path | None = None

class PluginConfig(BaseModel):
    install_dir: Path = Path("~/.config/vantagrid/plugins")
    enabled_plugins: list[str] = []
