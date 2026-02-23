"""Theme loading and cycling service."""
from __future__ import annotations

from vantagrid.models.theme import Theme as ThemeModel
from vantagrid.themes import THEMES, list_builtin_themes


class ThemeService:
    """Manages theme discovery and cycling."""

    def list_themes(self) -> list[ThemeModel]:
        """Get list of all available themes."""
        return [
            ThemeModel(
                name=name,
                label=name.replace("_", " ").title(),
                css_path="",  # No CSS files — using Textual Theme objects
                is_builtin=True,
            )
            for name in list_builtin_themes()
        ]

    def get_theme(self, name: str) -> ThemeModel | None:
        """Get a theme by name."""
        if name in THEMES:
            return ThemeModel(
                name=name,
                label=name.replace("_", " ").title(),
                css_path="",
                is_builtin=True,
            )
        return None

    def cycle_next(self, current: str) -> ThemeModel:
        """Get the next theme in the cycle."""
        available = list_builtin_themes()
        if not available:
            raise ValueError("No themes available")
        try:
            idx = available.index(current)
            next_name = available[(idx + 1) % len(available)]
        except ValueError:
            next_name = available[0]
        return ThemeModel(
            name=next_name,
            label=next_name.replace("_", " ").title(),
            css_path="",
            is_builtin=True,
        )
