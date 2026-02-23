"""Main Textual application for VantaGrid."""
from __future__ import annotations

from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive

from vantagrid.services.config_service import ConfigService
from vantagrid.themes import get_theme_path, list_builtin_themes
from vantagrid.widgets.terminal_pane import TerminalPane
from vantagrid.widgets.file_explorer import FileExplorer
from vantagrid.widgets.tab_bar import TabBar
from vantagrid.widgets.status_bar import StatusBar
from vantagrid.widgets.usage_panel import UsagePanel
from vantagrid.widgets.skill_browser import SkillBrowser
from vantagrid.widgets.theme_picker import ThemePicker
from vantagrid.widgets.command_palette import CommandPalette


class VantaGridApp(App):
    """Main application for VantaGrid terminal UI."""

    TITLE = "VantaGrid"
    BINDINGS = [
        Binding("ctrl+s", "swap_focus", "Swap", show=True),
        Binding("ctrl+t", "cycle_theme", "Theme", show=True),
        Binding("ctrl+b", "toggle_sidebar", "Sidebar", show=True),
        Binding("ctrl+j", "toggle_bottom", "Bottom", show=True),
        Binding("ctrl+p", "open_palette", "Palette", show=True),
        Binding("ctrl+k", "open_skills", "Skills", show=True),
        Binding("ctrl+q", "quit", "Quit", show=True),
    ]

    DEFAULT_CSS = """
    Screen {
        layout: vertical;
    }

    #sidebar {
        width: 20;
        border-right: 1 solid $primary;
        overflow: auto;
    }

    #main-container {
        height: 1fr;
        layout: vertical;
    }

    #tab-bar-container {
        height: 1;
        border-bottom: 1 solid $primary;
    }

    #content-area {
        height: 1fr;
        border-bottom: 1 solid $primary;
    }

    #bottom-panel {
        height: 8;
        border-top: 1 solid $primary;
        overflow: auto;
    }

    #status-bar {
        height: 1;
        border-top: 1 solid $primary;
    }
    """

    # Reactive attributes
    current_theme = reactive("synthwave")
    sidebar_visible = reactive(True)
    bottom_visible = reactive(True)

    def __init__(
        self,
        theme_name: str = "synthwave",
        layout_mode: str = "vscode",
        show_sidebar: bool = True,
        show_bottom: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.current_theme = theme_name
        self.sidebar_visible = show_sidebar
        self.bottom_visible = show_bottom
        self.config_service = ConfigService()
        self.config = self.config_service.load()

    def compose(self) -> ComposeResult:
        """Compose the main app layout."""
        yield Header()

        with Horizontal(id="main-container"):
            # Sidebar
            with Vertical(id="sidebar", display=self.sidebar_visible):
                yield FileExplorer(Path.home())
                yield ThemePicker()
                yield SkillBrowser()

            # Main content area
            with Vertical(id="main-container"):
                # Tab bar
                with Vertical(id="tab-bar-container"):
                    yield TabBar()

                # Terminal panes
                with Vertical(id="content-area"):
                    yield TerminalPane(account_name="DarkCode")
                    yield TerminalPane(account_name="haKCer")

                # Bottom panel
                with Vertical(id="bottom-panel", display=self.bottom_visible):
                    yield UsagePanel()

        # Status bar
        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize app on mount."""
        self._load_theme()
        self._initialize_status_bar()

    def _load_theme(self) -> None:
        """Load CSS for the current theme."""
        theme_path = get_theme_path(self.current_theme)
        with open(theme_path) as f:
            self.theme_css = f.read()

    def _initialize_status_bar(self) -> None:
        """Set up the status bar."""
        status_bar = self.query_one(StatusBar)
        status_bar.set_theme(self.current_theme)
        available_themes = list_builtin_themes()
        theme_picker = self.query_one(ThemePicker)
        theme_picker.set_themes(available_themes, self.current_theme)

    def watch_current_theme(self, theme_name: str) -> None:
        """Handle theme changes."""
        self._load_theme()
        status_bar = self.query_one(StatusBar)
        status_bar.set_theme(theme_name)
        theme_picker = self.query_one(ThemePicker)
        theme_picker.set_active_theme(theme_name)

    def watch_sidebar_visible(self, visible: bool) -> None:
        """Handle sidebar visibility changes."""
        sidebar = self.query_one("#sidebar", Vertical)
        sidebar.display = visible

    def watch_bottom_visible(self, visible: bool) -> None:
        """Handle bottom panel visibility changes."""
        bottom = self.query_one("#bottom-panel", Vertical)
        bottom.display = visible

    def action_swap_focus(self) -> None:
        """Swap focus to the next account's terminal."""
        panes = self.query(TerminalPane)
        if panes:
            current_focus = self.focused
            for i, pane in enumerate(panes):
                if pane == current_focus:
                    next_pane = panes[(i + 1) % len(panes)]
                    next_pane.focus()
                    return
            panes[0].focus()

    def action_cycle_theme(self) -> None:
        """Cycle to the next available theme."""
        available = list_builtin_themes()
        if not available:
            return
        try:
            current_idx = available.index(self.current_theme)
            next_idx = (current_idx + 1) % len(available)
            self.current_theme = available[next_idx]
        except ValueError:
            self.current_theme = available[0]

    def action_toggle_sidebar(self) -> None:
        """Toggle sidebar visibility."""
        self.sidebar_visible = not self.sidebar_visible

    def action_toggle_bottom(self) -> None:
        """Toggle bottom panel visibility."""
        self.bottom_visible = not self.bottom_visible

    def action_open_palette(self) -> None:
        """Open the command palette."""
        palette = CommandPalette()
        self.mount(palette)
        self.query_one(CommandPalette).focus()

    def action_open_skills(self) -> None:
        """Open the skills browser."""
        skill_browser = self.query_one(SkillBrowser)
        skill_browser.focus()

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

    def on_command_palette_command_selected(
        self, message: CommandPalette.CommandSelected
    ) -> None:
        """Handle command palette selection."""
        cmd = message.command_name
        if cmd == "swap_focus":
            self.action_swap_focus()
        elif cmd == "cycle_theme":
            self.action_cycle_theme()
        elif cmd == "toggle_sidebar":
            self.action_toggle_sidebar()
        elif cmd == "toggle_bottom":
            self.action_toggle_bottom()
        elif cmd == "open_skills":
            self.action_open_skills()
        elif cmd == "quit":
            self.action_quit()

    def on_theme_picker_theme_selected(
        self, message: ThemePicker.ThemeSelected
    ) -> None:
        """Handle theme selection from picker."""
        self.current_theme = message.theme_name


def main():
    """Entry point for the application."""
    app = VantaGridApp()
    app.run()


if __name__ == "__main__":
    main()
