"""Session Logger Plugin — logs session events to a file."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("~/.config/vantagrid/logs/sessions.jsonl").expanduser()

HOOKS = ["on_session_start", "on_switch"]


def on_session_start(account_name: str, session_id: str, **kwargs: object) -> None:
    """Log when a new session starts."""
    _log_event("session_start", account=account_name, session_id=session_id)


def on_switch(from_account: str, to_account: str, reason: str, **kwargs: object) -> None:
    """Log when accounts are switched."""
    _log_event("switch", from_account=from_account, to_account=to_account, reason=reason)


def _log_event(event_type: str, **data: object) -> None:
    """Append a JSON line to the log file."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {"type": event_type, "timestamp": datetime.now().isoformat(), **data}
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
