"""Terminal pane widget for displaying Claude Code PTY sessions."""
from __future__ import annotations

from textual.widget import Widget
from textual.containers import Container
from textual.widgets import Static, RichLog
from textual.reactive import reactive


class TerminalPane(Widget):
    """A widget wrapping a Claude Code PTY session display."""

    DEFAULT_CSS = """
    TerminalPane {
        height: 1fr;
        border: 1 solid #e94560;
    }

    .terminal-output {
        height: 1fr;
    }
    """

    account_name = reactive("")
    session_id = reactive("")

    def __init__(self, account_name: str = "", session_id: str = "", **kwargs):
        super().__init__(**kwargs)
        self.account_name = account_name
        self.session_id = session_id
        self._output = None

    def compose(self):
        """Compose the terminal pane with output display."""
        yield RichLog(classes="terminal-output")

    def on_mount(self):
        """Initialize terminal display on mount."""
        self._output = self.query_one(RichLog)
        self._update_border()

    def _update_border(self):
        """Update the border title with account and session info."""
        if self.account_name and self.session_id:
            title = f"{self.account_name} ({self.session_id})"
            self.border_title = title
        elif self.account_name:
            self.border_title = self.account_name

    def watch_account_name(self, name: str):
        """Update when account name changes."""
        self._update_border()

    def watch_session_id(self, sid: str):
        """Update when session ID changes."""
        self._update_border()

    def start_session(self, account_name: str, cwd: str = "/tmp"):
        """Start a new PTY session.

        Args:
            account_name: The account name to display
            cwd: Current working directory for the session
        """
        self.account_name = account_name
        self.session_id = "session-001"  # Placeholder

    def send_input(self, data: str):
        """Send input to the terminal session.

        Args:
            data: Input data to send
        """
        if self._output:
            self._output.write(data)

    def log_output(self, data: str):
        """Log output to the terminal display.

        Args:
            data: Output to display
        """
        if self._output:
            self._output.write(data)

    def stop(self):
        """Stop the PTY session."""
        self.account_name = ""
        self.session_id = ""
