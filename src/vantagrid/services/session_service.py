"""Session management service for PTY-based Claude Code sessions."""
from __future__ import annotations

import uuid
from pathlib import Path

from vantagrid.models.account import Account
from vantagrid.models.session import Session, SessionState
from vantagrid.utils.pty import PtyProcess, spawn_claude


class SessionService:
    """Manages PTY sessions for Claude Code instances."""

    def __init__(self) -> None:
        self._sessions: dict[str, tuple[Session, PtyProcess]] = {}

    def launch(self, account: Account, cwd: Path) -> Session:
        """Launch a new Claude Code session for an account."""
        session_id = uuid.uuid4().hex[:8]

        # Spawn the PTY process
        pty_proc = spawn_claude(account.config_dir, cwd)

        # Create session model
        session = Session(
            id=session_id,
            account_name=account.name,
            state=SessionState.RUNNING,
            pid=pty_proc.pid,
            working_dir=cwd,
        )

        # Store session
        self._sessions[session_id] = (session, pty_proc)

        return session

    def kill(self, session_id: str) -> None:
        """Kill a session by ID."""
        if session_id not in self._sessions:
            return

        session, pty_proc = self._sessions[session_id]
        pty_proc.kill()
        session.state = SessionState.STOPPED
        del self._sessions[session_id]

    def focus(self, session_id: str) -> None:
        """Mark a session as focused (active for I/O)."""
        if session_id in self._sessions:
            session, _ = self._sessions[session_id]
            session.state = SessionState.RUNNING

    def list_active(self) -> list[Session]:
        """Return list of active (running) sessions."""
        active = []
        to_remove = []

        for session_id, (session, pty_proc) in self._sessions.items():
            if pty_proc.is_alive():
                active.append(session)
            else:
                # Clean up dead sessions
                session.state = SessionState.STOPPED
                to_remove.append(session_id)

        for session_id in to_remove:
            del self._sessions[session_id]

        return active

    def get(self, session_id: str) -> Session | None:
        """Get a session by ID."""
        if session_id in self._sessions:
            session, _ = self._sessions[session_id]
            return session
        return None
