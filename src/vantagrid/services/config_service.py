"""Configuration management service."""
from __future__ import annotations

import sys
from pathlib import Path

from vantagrid.models.config import VantaGridConfig

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import tomli_w


class ConfigService:
    CONFIG_DIR = Path("~/.config/vantagrid").expanduser()

    @classmethod
    def config_path(cls) -> Path:
        return cls.CONFIG_DIR / "config.toml"

    def load(self) -> VantaGridConfig:
        """Load configuration from TOML file or return defaults."""
        path = self.config_path()
        if not path.exists():
            return VantaGridConfig()
        with open(path, "rb") as f:
            data = tomllib.load(f)
        return VantaGridConfig.model_validate(data)

    def save(self, config: VantaGridConfig) -> None:
        """Save configuration to TOML file."""
        path = self.config_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        data = config.model_dump(mode="json")
        with open(path, "wb") as f:
            tomli_w.dump(data, f)

    def save_default(self) -> None:
        """Save default configuration."""
        self.save(VantaGridConfig())
