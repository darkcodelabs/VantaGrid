"""CLI entry point for VantaGrid."""

from __future__ import annotations

import click

from vantagrid import __version__


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="vantagrid")
@click.option("--theme", "-t", default=None, help="Theme to use (e.g. synthwave, dracula)")
@click.option("--layout", "-l", default=None, type=click.Choice(["ide", "minimal"]))
@click.option("--no-sidebar", is_flag=True, help="Start without sidebar")
@click.option("--no-bottom", is_flag=True, help="Start without bottom panel")
@click.pass_context
def main(ctx: click.Context, theme: str | None, layout: str | None, no_sidebar: bool, no_bottom: bool) -> None:
    """VantaGrid — Terminal IDE for multi-account Claude Code."""
    if ctx.invoked_subcommand is not None:
        return

    from vantagrid.app import VantaGridApp

    app = VantaGridApp(
        theme_name=theme,
        layout_mode=layout,
        show_sidebar=not no_sidebar,
        show_bottom=not no_bottom,
    )
    app.run()


@main.command()
def config() -> None:
    """Open configuration file."""
    from vantagrid.services.config_service import ConfigService

    path = ConfigService.config_path()
    click.echo(f"Config: {path}")
    if not path.exists():
        ConfigService().save_default()
        click.echo("Created default config.")
    click.launch(str(path))


@main.command()
def themes() -> None:
    """List available themes."""
    from vantagrid.themes import list_builtin_themes

    click.echo("Built-in themes:")
    for name in list_builtin_themes():
        click.echo(f"  - {name}")


@main.command()
def accounts() -> None:
    """List discovered Claude Code accounts."""
    from vantagrid.services.account_service import AccountService

    svc = AccountService()
    for acct in svc.discover():
        status = " (active)" if acct.is_active else ""
        click.echo(f"  {acct.name} [{acct.plan}] {acct.config_dir}{status}")
