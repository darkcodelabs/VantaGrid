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

```bash
uv tool install vantagrid
```

## Usage

```bash
vantagrid    # or: vg
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
| `Ctrl+1/2` | Focus pane 1 or 2 |
| `Ctrl+Q` | Quit |

## Configuration

```bash
~/.config/vantagrid/config.toml
```

## Development

```bash
git clone https://github.com/darkcodelabs/VantaGrid
cd VantaGrid
uv sync --extra dev
pytest
```

## License

MIT
