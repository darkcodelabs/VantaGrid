"""Test AccountService."""
from __future__ import annotations

from pathlib import Path

import pytest

from vantagrid.services.account_service import AccountService


class TestAccountService:
    """Test AccountService."""

    def test_discover_no_accounts(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test discover returns empty list when no .claude dirs exist."""
        monkeypatch.setenv("HOME", str(tmp_path))
        service = AccountService()
        accounts = service.discover()
        assert accounts == []

    def test_discover_finds_default_claude(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test discover finds .claude directory."""
        monkeypatch.setenv("HOME", str(tmp_path))
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        service = AccountService()
        accounts = service.discover()

        assert len(accounts) == 1
        assert accounts[0].name == "default"
        assert accounts[0].config_dir == claude_dir

    def test_discover_finds_named_accounts(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test discover finds .claude-<name> directories."""
        monkeypatch.setenv("HOME", str(tmp_path))
        (tmp_path / ".claude").mkdir()
        (tmp_path / ".claude-work").mkdir()
        (tmp_path / ".claude-personal").mkdir()

        service = AccountService()
        accounts = service.discover()

        names = {acc.name for acc in accounts}
        assert "default" in names
        assert "work" in names
        assert "personal" in names

    def test_discover_ignores_files(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test discover ignores non-directory .claude* files."""
        monkeypatch.setenv("HOME", str(tmp_path))
        (tmp_path / ".claude").mkdir()
        (tmp_path / ".claude-file").touch()

        service = AccountService()
        accounts = service.discover()

        names = {acc.name for acc in accounts}
        assert "default" in names
        assert len(names) == 1

    def test_get_returns_correct_account(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test get returns correct account."""
        monkeypatch.setenv("HOME", str(tmp_path))
        work_dir = tmp_path / ".claude-work"
        work_dir.mkdir()
        (tmp_path / ".claude").mkdir()

        service = AccountService()
        account = service.get("work")

        assert account is not None
        assert account.name == "work"
        assert account.config_dir == work_dir

    def test_get_returns_none_for_missing(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test get returns None for non-existent account."""
        monkeypatch.setenv("HOME", str(tmp_path))
        (tmp_path / ".claude").mkdir()

        service = AccountService()
        account = service.get("nonexistent")

        assert account is None

    def test_activate_sets_is_active(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test activate sets is_active flag."""
        monkeypatch.setenv("HOME", str(tmp_path))
        (tmp_path / ".claude").mkdir()

        service = AccountService()
        account = service.activate("default")

        assert account.is_active is True
        assert account.name == "default"

    def test_activate_raises_for_missing(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test activate raises ValueError for non-existent account."""
        monkeypatch.setenv("HOME", str(tmp_path))
        (tmp_path / ".claude").mkdir()

        service = AccountService()
        with pytest.raises(ValueError, match="not found"):
            service.activate("nonexistent")

    def test_get_usage_returns_defaults(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test get_usage returns default AccountUsage when no file exists."""
        monkeypatch.setenv("HOME", str(tmp_path))
        (tmp_path / ".claude").mkdir()

        service = AccountService()
        usage = service.get_usage("default")

        assert usage.session_pct == 0.0
        assert usage.tokens_used == 0

    def test_get_usage_for_missing_account(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test get_usage for non-existent account returns defaults."""
        monkeypatch.setenv("HOME", str(tmp_path))
        (tmp_path / ".claude").mkdir()

        service = AccountService()
        usage = service.get_usage("nonexistent")

        assert usage.session_pct == 0.0
