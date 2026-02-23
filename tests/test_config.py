"""Test ConfigService."""
from __future__ import annotations

from pathlib import Path

import pytest

from vantagrid.models.config import AccountConfig, VantaGridConfig
from vantagrid.services.config_service import ConfigService


class TestConfigService:
    """Test ConfigService."""

    def test_config_path(self) -> None:
        """Test config_path returns correct path."""
        path = ConfigService.config_path()
        assert path.name == "config.toml"
        assert ".config/vantagrid" in str(path)

    def test_load_no_file_returns_defaults(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test load with no file returns default config."""
        config_dir = tmp_path / ".config" / "vantagrid"
        monkeypatch.setattr(ConfigService, "CONFIG_DIR", config_dir)

        service = ConfigService()
        config = service.load()

        assert isinstance(config, VantaGridConfig)
        assert config.theme == "synthwave"
        assert config.layout == "ide"
        assert config.accounts == {}

    def test_save_and_load_roundtrip(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test save and load roundtrip."""
        config_dir = tmp_path / ".config" / "vantagrid"
        monkeypatch.setattr(ConfigService, "CONFIG_DIR", config_dir)

        service = ConfigService()
        original = VantaGridConfig(
            theme="custom",
            layout="split",
            show_sidebar=False,
        )

        service.save(original)
        loaded = service.load()

        assert loaded.theme == "custom"
        assert loaded.layout == "split"
        assert loaded.show_sidebar is False

    def test_save_creates_directory(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test save creates config directory if needed."""
        config_dir = tmp_path / ".config" / "vantagrid"
        monkeypatch.setattr(ConfigService, "CONFIG_DIR", config_dir)

        service = ConfigService()
        config = VantaGridConfig()

        assert not config_dir.exists()
        service.save(config)
        assert config_dir.exists()

    def test_save_with_accounts(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test save and load with accounts."""
        config_dir = tmp_path / ".config" / "vantagrid"
        monkeypatch.setattr(ConfigService, "CONFIG_DIR", config_dir)

        service = ConfigService()
        account = AccountConfig(
            label="Test Account",
            config_dir=Path("/tmp/test"),
            plan="pro",
        )
        config = VantaGridConfig(accounts={"test": account})

        service.save(config)
        loaded = service.load()

        assert "test" in loaded.accounts
        assert loaded.accounts["test"].label == "Test Account"
        assert loaded.accounts["test"].plan == "pro"

    def test_save_default(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test save_default creates default config."""
        config_dir = tmp_path / ".config" / "vantagrid"
        monkeypatch.setattr(ConfigService, "CONFIG_DIR", config_dir)

        service = ConfigService()
        service.save_default()

        config_file = config_dir / "config.toml"
        assert config_file.exists()

        loaded = service.load()
        assert loaded.theme == "synthwave"
