"""Theme registry for VantaGrid — registers Textual Theme objects."""

from textual.theme import Theme

THEMES: dict[str, Theme] = {
    "synthwave": Theme(
        name="synthwave",
        primary="#e94560",
        secondary="#0f3460",
        accent="#00d4ff",
        background="#1a1a2e",
        surface="#16213e",
        panel="#0f3460",
        warning="#ffbe0b",
        error="#ff006e",
        success="#00d4ff",
        boost="#2a1a4e",
        dark=True,
    ),
    "dracula": Theme(
        name="dracula",
        primary="#bd93f9",
        secondary="#6272a4",
        accent="#8be9fd",
        foreground="#f8f8f2",
        background="#282a36",
        surface="#21222c",
        panel="#44475a",
        warning="#f1fa8c",
        error="#ff5555",
        success="#50fa7b",
        boost="#343746",
        dark=True,
    ),
    "nord": Theme(
        name="nord",
        primary="#88c0d0",
        secondary="#81a1c1",
        accent="#8fbcbb",
        foreground="#eceff4",
        background="#2e3440",
        surface="#3b4252",
        panel="#434c5e",
        warning="#ebcb8b",
        error="#bf616a",
        success="#a3be8c",
        boost="#4c566a",
        dark=True,
    ),
    "gruvbox": Theme(
        name="gruvbox",
        primary="#d79921",
        secondary="#458588",
        accent="#b16286",
        foreground="#ebdbb2",
        background="#282828",
        surface="#3c3836",
        panel="#504945",
        warning="#d79921",
        error="#cc241d",
        success="#98971a",
        boost="#665c54",
        dark=True,
    ),
    "tokyo_night": Theme(
        name="tokyo_night",
        primary="#7aa2f7",
        secondary="#7dcfff",
        accent="#bb9af7",
        foreground="#a9b1d6",
        background="#1a1b26",
        surface="#24283b",
        panel="#292e42",
        warning="#e0af68",
        error="#f7768e",
        success="#9ece6a",
        boost="#414868",
        dark=True,
    ),
    "cyberpunk": Theme(
        name="cyberpunk",
        primary="#00ff41",
        secondary="#00b4d8",
        accent="#ff006e",
        foreground="#e0e0e0",
        background="#0d0d0d",
        surface="#1a1a1a",
        panel="#262626",
        warning="#ffbe0b",
        error="#ff006e",
        success="#00ff41",
        boost="#333333",
        dark=True,
    ),
    "monochrome": Theme(
        name="monochrome",
        primary="#ffffff",
        secondary="#999999",
        accent="#ffffff",
        foreground="#e0e0e0",
        background="#1a1a1a",
        surface="#222222",
        panel="#333333",
        warning="#cccccc",
        error="#aaaaaa",
        success="#dddddd",
        boost="#444444",
        dark=True,
    ),
}

BUILTIN_THEMES = list(THEMES.keys())


def list_builtin_themes() -> list[str]:
    """List all built-in theme names."""
    return list(BUILTIN_THEMES)


def get_theme(name: str) -> Theme:
    """Get a Theme object by name."""
    if name not in THEMES:
        raise KeyError(f"Theme not found: {name}")
    return THEMES[name]
