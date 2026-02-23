"""Theme registry and loader for VantaGrid."""

from pathlib import Path

THEMES_DIR = Path(__file__).parent
BUILTIN_THEMES = [
    "synthwave",
    "dracula",
    "nord",
    "gruvbox",
    "tokyo_night",
    "cyberpunk",
    "monochrome",
]


def get_theme_path(name: str) -> Path:
    """Get the path to a built-in theme CSS file."""
    path = THEMES_DIR / f"{name}.tcss"
    if not path.exists():
        raise FileNotFoundError(f"Theme not found: {name}")
    return path


def list_builtin_themes() -> list[str]:
    """List all built-in theme names."""
    return list(BUILTIN_THEMES)
