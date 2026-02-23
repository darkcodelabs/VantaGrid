"""Theme loading and cycling service."""
from __future__ import annotations

from pathlib import Path

from vantagrid.models.theme import Theme


class ThemeService:
    """Manages theme discovery, loading, and cycling."""

    @staticmethod
    def get_builtins_dir() -> Path:
        """Get the bundled themes directory."""
        return Path(__file__).parent.parent / "themes" / "builtins"

    def list_themes(self) -> list[Theme]:
        """Get list of builtin and custom themes."""
        themes = []

        # Load builtin themes
        builtins_dir = self.get_builtins_dir()
        if builtins_dir.exists():
            for theme_dir in builtins_dir.iterdir():
                if theme_dir.is_dir():
                    css_file = theme_dir / "theme.tcss"
                    if css_file.exists():
                        theme = Theme(
                            name=theme_dir.name,
                            label=theme_dir.name.replace("_", " ").title(),
                            css_path=css_file,
                            is_builtin=True,
                            description="",
                        )
                        themes.append(theme)

        return themes

    def get_theme(self, name: str) -> Theme | None:
        """Get a theme by name."""
        for theme in self.list_themes():
            if theme.name == name:
                return theme
        return None

    def cycle_next(self, current: str) -> Theme:
        """Get the next theme in the cycle."""
        themes = self.list_themes()
        if not themes:
            raise ValueError("No themes available")

        current_index = -1
        for i, theme in enumerate(themes):
            if theme.name == current:
                current_index = i
                break

        next_index = (current_index + 1) % len(themes)
        return themes[next_index]

    def get_css(self, name: str) -> str:
        """Read and return the CSS file contents for a theme."""
        theme = self.get_theme(name)
        if not theme:
            raise ValueError(f"Theme '{name}' not found")

        with open(theme.css_path) as f:
            return f.read()

    def load_custom_themes(self, custom_dir: Path) -> list[Theme]:
        """Load custom themes from a directory."""
        custom_themes = []

        if not custom_dir.exists():
            return custom_themes

        for theme_dir in custom_dir.iterdir():
            if theme_dir.is_dir():
                css_file = theme_dir / "theme.tcss"
                if css_file.exists():
                    theme = Theme(
                        name=theme_dir.name,
                        label=theme_dir.name.replace("_", " ").title(),
                        css_path=css_file,
                        is_builtin=False,
                        description="",
                    )
                    custom_themes.append(theme)

        return custom_themes
