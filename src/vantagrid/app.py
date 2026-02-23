"""Main Textual application for VantaGrid."""
from __future__ import annotations

from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer

from vantagrid.services.config_service import ConfigService
from vantagrid.themes import THEMES, list_builtin_themes
from vantagrid.widgets.terminal_pane import TerminalPane
from vantagrid.widgets.file_explorer import FileExplorer
from vantagrid.widgets.tab_bar import TabBar
from vantagrid.widgets.status_bar import StatusBar
from vantagrid.widgets.usage_panel import UsagePanel
from vantagrid.widgets.skill_browser import SkillBrowser
from vantagrid.widgets.theme_picker import ThemePicker
from vantagrid.widgets.command_palette import CommandPalette
from vantagrid.widgets.image_viewer import ImageViewer


class VantaGridApp(App):
    """Terminal IDE for multi-account Claude Code."""

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
    #app-body {
        height: 1fr;
    }

    #sidebar {
        width: 28;
        border-right: solid $primary;
        overflow-y: auto;
    }

    #main-area {
        width: 1fr;
    }

    #tab-bar-area {
        height: 3;
    }

    #content-area {
        height: 1fr;
    }

    #bottom-panel {
        height: 10;
        border-top: solid $primary;
        overflow-y: auto;
    }

    #status-bar {
        height: 1;
    }
    """

    def __init__(
        self,
        theme_name: str | None = None,
        layout_mode: str | None = None,
        show_sidebar: bool = True,
        show_bottom: bool = True,
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)
        self._theme_name = theme_name or "synthwave"
        self._show_sidebar = show_sidebar
        self._show_bottom = show_bottom
        self.config_service = ConfigService()
        self.vg_config = self.config_service.load()

        # Register all VantaGrid themes with Textual
        for theme in THEMES.values():
            self.register_theme(theme)

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="app-body"):
            with Vertical(id="sidebar"):
                yield FileExplorer(Path.home())
                yield ThemePicker()
                yield SkillBrowser()

            with Vertical(id="main-area"):
                with Horizontal(id="tab-bar-area"):
                    yield TabBar()

                with Horizontal(id="content-area"):
                    yield TerminalPane(account_name="DarkCode", plan="5x")
                    yield TerminalPane(account_name="haKCer", plan="20x")

                with Vertical(id="bottom-panel"):
                    yield UsagePanel()

        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        # Apply the selected theme via Textual's theme system
        self.theme = self._theme_name
        self.query_one(StatusBar).set_theme(self._theme_name)
        if not self._show_sidebar:
            self.query_one("#sidebar").display = False
        if not self._show_bottom:
            self.query_one("#bottom-panel").display = False

        # Populate theme picker (after theme is applied)
        self.query_one(ThemePicker).set_themes(
            list_builtin_themes(), active=self._theme_name
        )

        # Add tabs
        tab_bar = self.query_one(TabBar)
        tab_bar.add_tab("darkcode", "☰ Claude Code (DarkCode)")
        tab_bar.add_tab("hakcer", "☰ Claude Code (haKCer)")

        # Seed usage panel
        usage = self.query_one(UsagePanel)
        usage.set_account_usage("DarkCode", 0.0)
        usage.set_account_usage("haKCer", 0.0)

    def action_swap_focus(self) -> None:
        panes = list(self.query(TerminalPane))
        if not panes:
            return
        focused = self.focused
        for i, pane in enumerate(panes):
            if pane == focused:
                panes[(i + 1) % len(panes)].focus()
                return
        panes[0].focus()

    def action_cycle_theme(self) -> None:
        available = list_builtin_themes()
        if not available:
            return
        current = self.theme if isinstance(self.theme, str) else self._theme_name
        try:
            idx = available.index(current)
            next_theme = available[(idx + 1) % len(available)]
        except ValueError:
            next_theme = available[0]
        self._theme_name = next_theme
        self.theme = next_theme
        self.query_one(StatusBar).set_theme(next_theme)
        self.query_one(ThemePicker).set_active_theme(next_theme)

    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one("#sidebar")
        sidebar.display = not sidebar.display

    def action_toggle_bottom(self) -> None:
        bottom = self.query_one("#bottom-panel")
        bottom.display = not bottom.display

    def action_open_palette(self) -> None:
        palette = CommandPalette()
        self.mount(palette)
        palette.focus()

    def action_open_skills(self) -> None:
        self.query_one(SkillBrowser).focus()

    def action_quit(self) -> None:
        self.exit()

    def on_command_palette_command_selected(
        self, message: CommandPalette.CommandSelected
    ) -> None:
        actions = {
            "swap_focus": self.action_swap_focus,
            "cycle_theme": self.action_cycle_theme,
            "toggle_sidebar": self.action_toggle_sidebar,
            "toggle_bottom": self.action_toggle_bottom,
            "open_skills": self.action_open_skills,
            "quit": self.action_quit,
        }
        action = actions.get(message.command_name)
        if action:
            action()

    def on_file_explorer_file_selected(
        self, message: FileExplorer.FileSelected
    ) -> None:
        """Handle file selection from the explorer."""
        path = message.path
        image_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
        if path.suffix.lower() in image_exts:
            viewer = ImageViewer(path)
            # Replace bottom panel content with image viewer
            bottom = self.query_one("#bottom-panel")
            for child in list(bottom.children):
                child.remove()
            bottom.mount(viewer)
            bottom.display = True

    def on_theme_picker_theme_selected(
        self, message: ThemePicker.ThemeSelected
    ) -> None:
        self._theme_name = message.theme_name
        self.theme = self._theme_name
        self.query_one(StatusBar).set_theme(self._theme_name)
        self.query_one(ThemePicker).set_active_theme(self._theme_name)
