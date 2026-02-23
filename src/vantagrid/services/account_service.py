"""Account discovery and management service."""
from __future__ import annotations

from pathlib import Path

from vantagrid.models.account import Account, AccountUsage


class AccountService:
    """Discovers and manages Claude Code accounts."""

    def discover(self) -> list[Account]:
        """Scan home directory for .claude* directories and create Account objects."""
        accounts = []
        home = Path.home()

        # Look for .claude and .claude-* directories
        for path in home.glob(".claude*"):
            if not path.is_dir():
                continue

            account_name = path.name[8:] if path.name.startswith(".claude-") else "default"
            if not account_name:
                account_name = "default"

            account = Account(
                name=account_name,
                config_dir=path,
                email="",
                plan="pro",
                is_active=False,
                usage=None,
            )
            accounts.append(account)

        return accounts

    def get(self, name: str) -> Account | None:
        """Get account by name from discovered accounts."""
        for account in self.discover():
            if account.name == name:
                return account
        return None

    def activate(self, name: str) -> Account:
        """Activate an account by name and return it."""
        accounts = self.discover()
        for account in accounts:
            if account.name == name:
                account.is_active = True
                return account
        raise ValueError(f"Account '{name}' not found")

    def get_usage(self, name: str) -> AccountUsage:
        """Get usage data for an account from its config directory."""
        account = self.get(name)
        if not account:
            return AccountUsage()

        config_dir = account.config_dir

        # Try to find and parse usage files in config directory
        # For now, return defaults if no usage file exists
        usage_file = config_dir / "usage.json"
        if usage_file.exists():
            try:
                import json

                with open(usage_file) as f:
                    data = json.load(f)
                return AccountUsage.model_validate(data)
            except Exception:
                pass

        # Return default AccountUsage
        return AccountUsage()
