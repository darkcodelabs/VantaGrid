"""Terminal pane widget for displaying Claude Code PTY sessions."""
from __future__ import annotations

from textual.containers import Vertical
from textual.widgets import Static, RichLog, Input
from textual.message import Message


class TerminalPane(Vertical):
    """A terminal pane with command input and output display."""

    class InputSubmitted(Message):
        """Posted when user submits input."""

        def __init__(self, text: str, account_name: str):
            super().__init__()
            self.text = text
            self.account_name = account_name

    DEFAULT_CSS = """
    TerminalPane {
        height: 1fr;
        width: 1fr;
        border: round $primary;
    }

    TerminalPane:focus-within {
        border: round $accent;
    }

    .terminal-header {
        height: 1;
        background: $panel;
        color: $text;
        text-style: bold;
        padding: 0 1;
        content-align: left middle;
    }

    .terminal-output {
        height: 1fr;
        overflow: auto;
    }

    .terminal-input {
        height: 1;
        border-top: solid $panel;
    }
    """

    def __init__(self, account_name: str = "", plan: str = "", **kwargs):
        super().__init__(**kwargs)
        self.account_name = account_name
        self.plan = plan

    def compose(self):
        """Compose the terminal pane."""
        yield Static(self.account_name or "Terminal", classes="terminal-header")
        yield RichLog(markup=True, highlight=True, classes="terminal-output")
        yield Input(classes="terminal-input")

    def on_mount(self):
        """Initialize terminal on mount."""
        label = self.account_name
        if self.plan:
            label += f" ({self.plan})"
        self.border_title = f" {label} "
        output = self.query_one(RichLog)
        output.write(f"[bold]Claude Code[/] — {self.account_name}")
        output.write("")
        output.write("[dim]// TODO: Everything. Let's start.[/]")
        output.write("")
        output.write("[dim]Use Claude Code in the terminal.[/]")
        output.write("[dim]Esc to focus or unfocus Claude.[/]")
        output.write("")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command submission."""
        text = event.value
        output = self.query_one(RichLog)
        input_widget = self.query_one(Input)

        # Echo the command
        if text:
            output.write(f"$ {text}\n")
            self.post_message(self.InputSubmitted(text, self.account_name))

        # Clear input
        input_widget.value = ""

    def log_output(self, data: str) -> None:
        """Log output to the terminal display.

        Args:
            data: Output to display
        """
        output = self.query_one(RichLog)
        output.write(data)
