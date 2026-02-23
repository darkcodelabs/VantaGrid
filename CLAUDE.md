# VantaGrid — CLAUDE.md

## Project Overview
Terminal IDE for multi-account Claude Code. Built with Textual (Python TUI framework).

## Architecture
- **Framework**: Textual (reactive Python TUI)
- **Models**: Pydantic v2 (typed, validated)
- **Services**: Typed service classes (no HTTP — direct calls)
- **Themes**: Textual CSS (.tcss files)

## Key Paths
- `src/vantagrid/` — main package
- `src/vantagrid/models/` — Pydantic models
- `src/vantagrid/services/` — business logic
- `src/vantagrid/widgets/` — Textual UI components
- `src/vantagrid/themes/` — .tcss theme files
- `tests/` — pytest tests

## Commands
```bash
# Run the app
uv run vantagrid

# Run tests
uv run pytest

# Type check
uv run mypy src/vantagrid

# Lint
uv run ruff check src/vantagrid
```

## Conventions
- All models use Pydantic v2 BaseModel with Field validators
- Services are plain classes with typed methods
- Widgets extend Textual Widget classes
- Config is TOML at ~/.config/vantagrid/config.toml
- No web server — Textual app calls services directly
