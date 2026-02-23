from __future__ import annotations
from pathlib import Path
from pydantic import BaseModel

class Theme(BaseModel):
    name: str
    label: str
    css_path: Path
    is_builtin: bool = True
    description: str = ""

class ThemeConfig(BaseModel):
    active_theme: str = "synthwave"
    custom_themes_dir: Path | None = None
