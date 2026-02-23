from __future__ import annotations
from pathlib import Path
from pydantic import BaseModel, Field

class AccountConfig(BaseModel):
    label: str
    config_dir: Path
    plan: str = "pro"

class SwitchingConfig(BaseModel):
    enabled: bool = True
    warn_threshold: float = Field(default=0.75, ge=0.0, le=1.0)
    auto_switch_threshold: float = Field(default=0.90, ge=0.0, le=1.0)
    cooldown_seconds: int = Field(default=30, ge=0)

class SkillsConfig(BaseModel):
    registry_url: str | None = "https://raw.githubusercontent.com/VantaGrid/skills/main/registry.json"
    install_dir: Path = Path("~/.claude/skills")

class HotkeysConfig(BaseModel):
    swap_focus: str = "ctrl+s"
    cycle_theme: str = "ctrl+t"
    toggle_sidebar: str = "ctrl+b"
    toggle_bottom: str = "ctrl+j"
    command_palette: str = "ctrl+p"
    open_skills: str = "ctrl+k"
    quit: str = "ctrl+q"

class VantaGridConfig(BaseModel):
    theme: str = "synthwave"
    layout: str = "ide"
    show_sidebar: bool = True
    show_bottom_panel: bool = True
    refresh_rate: int = Field(default=5, ge=1)
    accounts: dict[str, AccountConfig] = {}
    switching: SwitchingConfig = SwitchingConfig()
    skills: SkillsConfig = SkillsConfig()
    hotkeys: HotkeysConfig = HotkeysConfig()
    plugin_dir: Path = Path("~/.config/vantagrid/plugins")
