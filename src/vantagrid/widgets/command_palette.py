"""Command palette widget for executing commands via keyboard."""
from __future__ import annotations

from textual.widgets import Static, Input
from textual.containers import Vertical
from textual.message import Message
from difflib import SequenceMatcher


class CommandPalette(Vertical):
    """Full-screen overlay command palette with fuzzy search."""

    class CommandSelected(Message):
        """Posted when a command is selected."""

        def __init__(self, command_name: str):
            super().__init__()
            self.command_name = command_name

    DEFAULT_CSS = """
    CommandPalette {
        width: 100%;
        height: 100%;
        background: rgba(26, 26, 46, 0.95);
        border: 1 solid $primary;
        align: center top;
        overlay: screen;
    }

    .palette-container {
        width: 80;
        height: auto;
        border: 1 solid $accent;
        background: $panel;
        margin-top: 5;
    }

    #palette-input {
        width: 1fr;
        height: 1;
        border: 1 solid $accent;
        border-bottom: 2 solid $accent;
    }

    .palette-results {
        height: auto;
        max-height: 10;
        overflow: auto;
    }

    .palette-item {
        height: 1;
        padding: 0 1;
        color: $text-muted;
    }

    .palette-item--selected {
        background: $accent;
        color: $panel;
        text-style: bold;
    }
    """

    COMMANDS = [
        ("swap_focus", "Swap focus to next account"),
        ("cycle_theme", "Cycle to next theme"),
        ("toggle_sidebar", "Toggle sidebar visibility"),
        ("toggle_bottom", "Toggle bottom panel visibility"),
        ("open_skills", "Open skills browser"),
        ("open_plugins", "Open plugins browser"),
        ("quit", "Quit VantaGrid"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_index = 0
        self.filtered_commands = list(self.COMMANDS)

    def compose(self):
        """Compose the command palette."""
        with Vertical(classes="palette-container"):
            yield Input(
                placeholder="Search commands...",
                id="palette-input",
            )
            yield Static("", id="palette-results", classes="palette-results")

    def on_mount(self):
        """Focus the input on mount."""
        self.query_one("#palette-input", Input).focus()
        self._render_results()

    def on_input_changed(self, event: Input.Changed):
        """Filter commands as user types."""
        query = event.value.lower()
        if query:
            self.filtered_commands = [
                cmd
                for cmd in self.COMMANDS
                if self._fuzzy_match(query, cmd[0]) or self._fuzzy_match(query, cmd[1])
            ]
        else:
            self.filtered_commands = list(self.COMMANDS)
        self.selected_index = 0
        self._render_results()

    def on_input_submitted(self, event: Input.Submitted):
        """Execute selected command."""
        if self.filtered_commands:
            cmd_name, _ = self.filtered_commands[self.selected_index]
            self.post_message(self.CommandSelected(cmd_name))
            self.remove()

    def on_key(self, event):
        """Handle navigation keys."""
        if event.key == "up":
            self.selected_index = max(0, self.selected_index - 1)
            self._render_results()
        elif event.key == "down":
            self.selected_index = min(
                len(self.filtered_commands) - 1, self.selected_index + 1
            )
            self._render_results()
        elif event.key == "escape":
            self.remove()

    def _render_results(self):
        """Render filtered command results."""
        results = self.query_one("#palette-results", Static)
        lines = []
        for idx, (cmd_name, cmd_desc) in enumerate(self.filtered_commands):
            class_name = (
                "palette-item palette-item--selected"
                if idx == self.selected_index
                else "palette-item"
            )
            lines.append(f"[{class_name}]{cmd_name:<20} {cmd_desc}[/]")
        results.update("\n".join(lines))

    def _fuzzy_match(self, query: str, text: str) -> bool:
        """Simple fuzzy matching."""
        ratio = SequenceMatcher(None, query, text.lower()).ratio()
        return ratio > 0.3
