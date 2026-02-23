"""Test SessionService."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from vantagrid.models.account import Account
from vantagrid.models.session import SessionState
from vantagrid.services.session_service import SessionService


class TestSessionService:
    """Test SessionService."""

    @patch("vantagrid.services.session_service.spawn_claude")
    def test_launch_creates_session(self, mock_spawn: MagicMock, tmp_path: Path) -> None:
        """Test launch creates session and stores it."""
        mock_pty = MagicMock()
        mock_pty.pid = 12345
        mock_spawn.return_value = mock_pty

        service = SessionService()
        account = Account(name="test", config_dir=tmp_path / ".claude")
        cwd = tmp_path

        session = service.launch(account, cwd)

        assert session.id is not None
        assert session.account_name == "test"
        assert session.state == SessionState.RUNNING
        assert session.pid == 12345
        assert session.working_dir == cwd

    @patch("vantagrid.services.session_service.spawn_claude")
    def test_kill_removes_session(self, mock_spawn: MagicMock, tmp_path: Path) -> None:
        """Test kill removes session and marks as stopped."""
        mock_pty = MagicMock()
        mock_pty.pid = 12345
        mock_pty.is_alive.return_value = True
        mock_spawn.return_value = mock_pty

        service = SessionService()
        account = Account(name="test", config_dir=tmp_path / ".claude")
        cwd = tmp_path

        session = service.launch(account, cwd)
        session_id = session.id

        assert service.get(session_id) is not None
        service.kill(session_id)

        assert service.get(session_id) is None
        mock_pty.kill.assert_called_once()

    @patch("vantagrid.services.session_service.spawn_claude")
    def test_kill_nonexistent_session(self, mock_spawn: MagicMock) -> None:
        """Test kill on non-existent session does nothing."""
        service = SessionService()
        service.kill("nonexistent")

    @patch("vantagrid.services.session_service.spawn_claude")
    def test_focus_marks_running(self, mock_spawn: MagicMock, tmp_path: Path) -> None:
        """Test focus marks session as running."""
        mock_pty = MagicMock()
        mock_pty.pid = 12345
        mock_spawn.return_value = mock_pty

        service = SessionService()
        account = Account(name="test", config_dir=tmp_path / ".claude")
        cwd = tmp_path

        session = service.launch(account, cwd)
        session_id = session.id
        session.state = SessionState.IDLE

        service.focus(session_id)

        focused = service.get(session_id)
        assert focused is not None
        assert focused.state == SessionState.RUNNING

    @patch("vantagrid.services.session_service.spawn_claude")
    def test_list_active_returns_running(self, mock_spawn: MagicMock, tmp_path: Path) -> None:
        """Test list_active returns running sessions."""
        mock_pty1 = MagicMock()
        mock_pty1.pid = 12345
        mock_pty1.is_alive.return_value = True

        mock_pty2 = MagicMock()
        mock_pty2.pid = 12346
        mock_pty2.is_alive.return_value = False

        mock_spawn.side_effect = [mock_pty1, mock_pty2]

        service = SessionService()
        account = Account(name="test", config_dir=tmp_path / ".claude")
        cwd = tmp_path

        session1 = service.launch(account, cwd)
        session2 = service.launch(account, cwd)

        active = service.list_active()

        assert len(active) == 1
        assert active[0].id == session1.id

    @patch("vantagrid.services.session_service.spawn_claude")
    def test_list_active_cleans_dead(self, mock_spawn: MagicMock, tmp_path: Path) -> None:
        """Test list_active cleans up dead sessions."""
        mock_pty = MagicMock()
        mock_pty.pid = 12345
        mock_pty.is_alive.return_value = False
        mock_spawn.return_value = mock_pty

        service = SessionService()
        account = Account(name="test", config_dir=tmp_path / ".claude")
        cwd = tmp_path

        session = service.launch(account, cwd)
        session_id = session.id

        assert service.get(session_id) is not None
        active = service.list_active()

        assert len(active) == 0
        assert service.get(session_id) is None

    @patch("vantagrid.services.session_service.spawn_claude")
    def test_get_session(self, mock_spawn: MagicMock, tmp_path: Path) -> None:
        """Test get returns correct session."""
        mock_pty = MagicMock()
        mock_pty.pid = 12345
        mock_spawn.return_value = mock_pty

        service = SessionService()
        account = Account(name="test", config_dir=tmp_path / ".claude")
        cwd = tmp_path

        session = service.launch(account, cwd)

        retrieved = service.get(session.id)
        assert retrieved is not None
        assert retrieved.id == session.id
        assert retrieved.account_name == "test"

    def test_get_nonexistent(self) -> None:
        """Test get returns None for non-existent session."""
        service = SessionService()
        assert service.get("nonexistent") is None
