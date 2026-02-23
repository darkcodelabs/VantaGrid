# VantaGrid

Terminal IDE for multi-account Claude Code — split sessions, usage monitoring, skills, themes.

## Features

- **VS Code-style layout** — sidebar, tabbed sessions, bottom panel, status bar
- **Multi-account** — run multiple Claude Code accounts side-by-side
- **Usage monitoring** — live progress bars, burn rate, auto-switch at thresholds
- **Skills marketplace** — browse, preview, click-to-install Claude Code skills
- **Theme system** — 7 built-in themes, hot-swappable with Ctrl+T
- **Command palette** — Ctrl+P fuzzy search for any action
- **Mouse support** — click, drag to resize, scroll, hover
- **Cross-platform** — Pi ARM64, Ubuntu x86_64, macOS

## Install

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or pip

### Clone & Install

```bash
git clone https://github.com/darkcodelabs/VantaGrid.git ~/VantaGrid
cd ~/VantaGrid
uv sync
```

### Run

```bash
# From the project directory
uv run vg

# Or with full name
uv run vantagrid
```

### Install Globally (optional)

To make `vg` available anywhere without `uv run`:

```bash
uv tool install ~/VantaGrid
vg
```

To uninstall:

```bash
uv tool uninstall vantagrid
```

## Usage

```bash
vg                      # launch with defaults
vg --theme dracula      # launch with a specific theme
vg --no-sidebar         # launch without the sidebar
vg --no-bottom          # launch without the bottom panel
vg themes               # list available themes
vg accounts             # show discovered Claude Code accounts
vg config               # open config file location
```

## Hotkeys

| Key | Action |
|-----|--------|
| `Ctrl+S` | Swap focus between terminal panes |
| `Ctrl+T` | Cycle theme |
| `Ctrl+B` | Toggle sidebar |
| `Ctrl+J` | Toggle bottom panel |
| `Ctrl+P` | Command palette |
| `Ctrl+K` | Open skill browser |
| `Ctrl+Q` | Quit |

## Themes

7 built-in themes: **synthwave** (default), **dracula**, **nord**, **gruvbox**, **tokyo_night**, **cyberpunk**, **monochrome**

Cycle with `Ctrl+T` or pick from the sidebar.

## Configuration

```bash
~/.config/vantagrid/config.toml
```

Run `vg config` to open or create the config file.

## Development

```bash
git clone https://github.com/darkcodelabs/VantaGrid.git ~/VantaGrid
cd ~/VantaGrid
uv sync --extra dev
uv run pytest
uv run ruff check src/vantagrid
```

## License

MIT
