"""File explorer widget for browsing the directory tree."""
from __future__ import annotations

from pathlib import Path
from textual.widgets import DirectoryTree, Static
from textual.message import Message
from textual.containers import Vertical


class FileExplorer(Vertical):
    """Wraps DirectoryTree for filesystem browsing."""

    class FileSelected(Message):
        """Posted when a file is selected."""

        def __init__(self, path: Path):
            super().__init__()
            self.path = path

    DEFAULT_CSS = """
    FileExplorer {
        height: 1fr;
        overflow: auto;
        border: 1 solid #e94560;
    }

    .explorer-title {
        height: 1;
        content-align: left middle;
        background: $panel;
        color: $text;
        text-style: bold;
        padding: 0 1;
    }

    FileExplorer DirectoryTree {
        height: 1fr;
    }
    """

    def __init__(self, path: str | Path = "/", **kwargs):
        super().__init__(**kwargs)
        self.root_path = Path(path) if isinstance(path, str) else path

    def compose(self):
        """Compose the file explorer."""
        yield Static("EXPLORER", classes="explorer-title")
        yield DirectoryTree(self.root_path)

    def on_directory_tree_file_selected(self, event):
        """Handle file selection in the directory tree."""
        self.post_message(self.FileSelected(event.file_path))

    def set_root(self, path: str | Path):
        """Change the root directory."""
        self.root_path = Path(path) if isinstance(path, str) else path
        tree = self.query_one(DirectoryTree)
        tree.path = self.root_path
