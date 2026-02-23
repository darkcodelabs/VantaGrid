"""Test Pydantic models."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from vantagrid.models.account import Account, AccountUsage
from vantagrid.models.config import (
    AccountConfig,
    HotkeysConfig,
    SkillsConfig,
    SwitchingConfig,
    VantaGridConfig,
)
from vantagrid.models.plugin import PluginHook
from vantagrid.models.session import Session, SessionState, SessionSwitch
from vantagrid.models.skill import Skill, SkillRegistry
from vantagrid.models.theme import Theme, ThemeConfig
from vantagrid.models.usage import BurnRate, UsageHistory, UsageSnapshot


class TestAccountUsage:
    """Test AccountUsage model."""

    def test_create_with_defaults(self) -> None:
        """Test creation with all defaults."""
        usage = AccountUsage()
        assert usage.session_pct == 0.0
        assert usage.weekly_all_pct == 0.0
        assert usage.weekly_sonnet_pct == 0.0
        assert usage.tokens_used == 0
        assert usage.cost_usd == 0.0
        assert usage.messages == 0
        assert usage.reset_at is None
        assert isinstance(usage.updated_at, datetime)

    def test_create_with_values(self) -> None:
        """Test creation with custom values."""
        now = datetime.now()
        usage = AccountUsage(
            session_pct=0.5,
            weekly_all_pct=0.6,
            weekly_sonnet_pct=0.3,
            tokens_used=1000,
            cost_usd=5.0,
            messages=10,
            reset_at=now,
            updated_at=now,
        )
        assert usage.session_pct == 0.5
        assert usage.weekly_all_pct == 0.6
        assert usage.weekly_sonnet_pct == 0.3
        assert usage.tokens_used == 1000
        assert usage.cost_usd == 5.0
        assert usage.messages == 10

    def test_validation_pct_range(self) -> None:
        """Test percentage field validation."""
        with pytest.raises(ValueError):
            AccountUsage(session_pct=1.5)

        with pytest.raises(ValueError):
            AccountUsage(weekly_all_pct=-0.1)

    def test_serialization(self) -> None:
        """Test model_dump and model_dump_json."""
        usage = AccountUsage(session_pct=0.5, tokens_used=100)
        data = usage.model_dump()
        assert data["session_pct"] == 0.5
        assert data["tokens_used"] == 100

        json_str = usage.model_dump_json()
        assert isinstance(json_str, str)
        assert "session_pct" in json_str


class TestAccount:
    """Test Account model."""

    def test_create_minimal(self) -> None:
        """Test creation with required fields only."""
        config_dir = Path("/tmp/test")
        account = Account(name="test", config_dir=config_dir)
        assert account.name == "test"
        assert account.config_dir == config_dir
        assert account.email == ""
        assert account.plan == "pro"
        assert account.is_active is False
        assert account.usage is None

    def test_create_with_values(self) -> None:
        """Test creation with all fields."""
        config_dir = Path("/tmp/test")
        usage = AccountUsage(session_pct=0.5)
        account = Account(
            name="test",
            email="test@example.com",
            plan="20x",
            config_dir=config_dir,
            is_active=True,
            usage=usage,
        )
        assert account.name == "test"
        assert account.email == "test@example.com"
        assert account.plan == "20x"
        assert account.is_active is True
        assert account.usage == usage

    def test_plan_validation(self) -> None:
        """Test plan field validation."""
        config_dir = Path("/tmp/test")
        valid_plans = ["free", "pro", "5x", "20x"]
        for plan in valid_plans:
            account = Account(name="test", config_dir=config_dir, plan=plan)
            assert account.plan == plan

        with pytest.raises(ValueError):
            Account(name="test", config_dir=config_dir, plan="invalid")


class TestSessionState:
    """Test SessionState enum."""

    def test_enum_values(self) -> None:
        """Test all enum values exist."""
        assert SessionState.STARTING.value == "starting"
        assert SessionState.RUNNING.value == "running"
        assert SessionState.IDLE.value == "idle"
        assert SessionState.STOPPED.value == "stopped"


class TestSession:
    """Test Session model."""

    def test_create_minimal(self) -> None:
        """Test creation with required fields."""
        session = Session(id="test123", account_name="test")
        assert session.id == "test123"
        assert session.account_name == "test"
        assert session.state == SessionState.STARTING
        assert session.pid is None
        assert isinstance(session.started_at, datetime)
        assert isinstance(session.working_dir, Path)

    def test_create_with_values(self) -> None:
        """Test creation with all fields."""
        now = datetime.now()
        cwd = Path("/tmp")
        session = Session(
            id="test123",
            account_name="test",
            state=SessionState.RUNNING,
            pid=12345,
            started_at=now,
            working_dir=cwd,
        )
        assert session.pid == 12345
        assert session.state == SessionState.RUNNING
        assert session.working_dir == cwd


class TestSessionSwitch:
    """Test SessionSwitch model."""

    def test_create(self) -> None:
        """Test creation."""
        switch = SessionSwitch(
            from_account="acc1",
            to_account="acc2",
            reason="High usage",
        )
        assert switch.from_account == "acc1"
        assert switch.to_account == "acc2"
        assert switch.reason == "High usage"
        assert isinstance(switch.switched_at, datetime)


class TestUsageSnapshot:
    """Test UsageSnapshot model."""

    def test_create(self) -> None:
        """Test creation."""
        snapshot = UsageSnapshot(
            account_name="test",
            session_pct=0.5,
            weekly_pct=0.6,
        )
        assert snapshot.account_name == "test"
        assert snapshot.session_pct == 0.5
        assert snapshot.weekly_pct == 0.6
        assert isinstance(snapshot.timestamp, datetime)

    def test_validation_pct_range(self) -> None:
        """Test percentage validation."""
        with pytest.raises(ValueError):
            UsageSnapshot(
                account_name="test",
                session_pct=1.5,
                weekly_pct=0.5,
            )


class TestBurnRate:
    """Test BurnRate model."""

    def test_create_defaults(self) -> None:
        """Test creation with defaults."""
        rate = BurnRate(account_name="test")
        assert rate.account_name == "test"
        assert rate.pct_per_minute == 0.0
        assert rate.estimated_depletion_minutes is None

    def test_create_with_values(self) -> None:
        """Test creation with values."""
        rate = BurnRate(
            account_name="test",
            pct_per_minute=0.1,
            estimated_depletion_minutes=600.0,
        )
        assert rate.pct_per_minute == 0.1
        assert rate.estimated_depletion_minutes == 600.0


class TestUsageHistory:
    """Test UsageHistory model."""

    def test_create_defaults(self) -> None:
        """Test creation with defaults."""
        history = UsageHistory()
        assert history.snapshots == []
        assert history.max_snapshots == 100

    def test_add_snapshot(self) -> None:
        """Test adding snapshots."""
        history = UsageHistory()
        snapshot = UsageSnapshot(account_name="test", session_pct=0.5, weekly_pct=0.6)
        history.add(snapshot)
        assert len(history.snapshots) == 1
        assert history.snapshots[0] == snapshot

    def test_max_snapshots_truncation(self) -> None:
        """Test max_snapshots truncation."""
        history = UsageHistory(max_snapshots=3)
        for i in range(5):
            snapshot = UsageSnapshot(
                account_name="test",
                session_pct=i * 0.1,
                weekly_pct=i * 0.1,
            )
            history.add(snapshot)

        assert len(history.snapshots) == 3
        assert history.snapshots[0].session_pct == 0.2
        assert history.snapshots[2].session_pct == 0.4


class TestTheme:
    """Test Theme model."""

    def test_create(self) -> None:
        """Test creation."""
        theme = Theme(
            name="synthwave",
            label="Synthwave",
            css_path=Path("/tmp/synthwave.css"),
        )
        assert theme.name == "synthwave"
        assert theme.label == "Synthwave"
        assert theme.is_builtin is True
        assert theme.description == ""

    def test_create_with_values(self) -> None:
        """Test creation with all fields."""
        theme = Theme(
            name="custom",
            label="Custom Theme",
            css_path=Path("/tmp/custom.css"),
            is_builtin=False,
            description="A custom theme",
        )
        assert theme.is_builtin is False
        assert theme.description == "A custom theme"


class TestThemeConfig:
    """Test ThemeConfig model."""

    def test_create_defaults(self) -> None:
        """Test creation with defaults."""
        config = ThemeConfig()
        assert config.active_theme == "synthwave"
        assert config.custom_themes_dir is None

    def test_create_with_values(self) -> None:
        """Test creation with values."""
        config = ThemeConfig(
            active_theme="custom",
            custom_themes_dir=Path("/tmp/themes"),
        )
        assert config.active_theme == "custom"
        assert config.custom_themes_dir == Path("/tmp/themes")


class TestSkill:
    """Test Skill model."""

    def test_create_defaults(self) -> None:
        """Test creation with required fields."""
        skill = Skill(name="test", description="Test skill")
        assert skill.name == "test"
        assert skill.description == "Test skill"
        assert skill.version == "1.0.0"
        assert skill.source == "builtin"
        assert skill.installed is False
        assert skill.install_path is None
        assert skill.tags == []

    def test_create_with_values(self) -> None:
        """Test creation with all fields."""
        skill = Skill(
            name="test",
            description="Test skill",
            version="2.0.0",
            source="custom",
            installed=True,
            install_path=Path("/tmp/test"),
            tags=["tag1", "tag2"],
        )
        assert skill.version == "2.0.0"
        assert skill.source == "custom"
        assert skill.installed is True
        assert skill.tags == ["tag1", "tag2"]


class TestSkillRegistry:
    """Test SkillRegistry model."""

    def test_create_defaults(self) -> None:
        """Test creation with defaults."""
        registry = SkillRegistry()
        assert registry.skills == []
        assert registry.last_fetched is None
        assert registry.registry_url is None

    def test_create_with_skills(self) -> None:
        """Test creation with skills."""
        skill1 = Skill(name="test1", description="Test 1")
        skill2 = Skill(name="test2", description="Test 2")
        registry = SkillRegistry(skills=[skill1, skill2])
        assert len(registry.skills) == 2


class TestPluginHook:
    """Test PluginHook enum."""

    def test_enum_values(self) -> None:
        """Test all enum values."""
        assert PluginHook.ON_SESSION_START.value == "on_session_start"
        assert PluginHook.ON_SWITCH.value == "on_switch"
        assert PluginHook.ON_USAGE_UPDATE.value == "on_usage_update"
        assert PluginHook.ON_THEME_CHANGE.value == "on_theme_change"


class TestSwitchingConfig:
    """Test SwitchingConfig model."""

    def test_create_defaults(self) -> None:
        """Test creation with defaults."""
        config = SwitchingConfig()
        assert config.enabled is True
        assert config.warn_threshold == 0.75
        assert config.auto_switch_threshold == 0.90
        assert config.cooldown_seconds == 30

    def test_validation(self) -> None:
        """Test field validation."""
        with pytest.raises(ValueError):
            SwitchingConfig(warn_threshold=1.5)

        with pytest.raises(ValueError):
            SwitchingConfig(cooldown_seconds=-1)


class TestSkillsConfig:
    """Test SkillsConfig model."""

    def test_create_defaults(self) -> None:
        """Test creation with defaults."""
        config = SkillsConfig()
        assert config.registry_url is not None
        assert config.install_dir == Path("~/.claude/skills")


class TestHotkeysConfig:
    """Test HotkeysConfig model."""

    def test_create_defaults(self) -> None:
        """Test creation with all defaults."""
        config = HotkeysConfig()
        assert config.swap_focus == "ctrl+s"
        assert config.cycle_theme == "ctrl+t"
        assert config.toggle_sidebar == "ctrl+b"
        assert config.toggle_bottom == "ctrl+j"
        assert config.command_palette == "ctrl+p"
        assert config.open_skills == "ctrl+k"
        assert config.quit == "ctrl+q"


class TestAccountConfig:
    """Test AccountConfig model."""

    def test_create(self) -> None:
        """Test creation."""
        config = AccountConfig(
            label="Main",
            config_dir=Path("/tmp/test"),
        )
        assert config.label == "Main"
        assert config.config_dir == Path("/tmp/test")
        assert config.plan == "pro"

    def test_create_with_plan(self) -> None:
        """Test creation with custom plan."""
        config = AccountConfig(
            label="Main",
            config_dir=Path("/tmp/test"),
            plan="5x",
        )
        assert config.plan == "5x"


class TestVantaGridConfig:
    """Test VantaGridConfig model."""

    def test_create_defaults(self) -> None:
        """Test creation with all defaults."""
        config = VantaGridConfig()
        assert config.theme == "synthwave"
        assert config.layout == "ide"
        assert config.show_sidebar is True
        assert config.show_bottom_panel is True
        assert config.refresh_rate == 5
        assert config.accounts == {}
        assert isinstance(config.switching, SwitchingConfig)
        assert isinstance(config.skills, SkillsConfig)
        assert isinstance(config.hotkeys, HotkeysConfig)

    def test_create_with_accounts(self) -> None:
        """Test creation with accounts."""
        account = AccountConfig(
            label="Test",
            config_dir=Path("/tmp/test"),
        )
        config = VantaGridConfig(accounts={"test": account})
        assert "test" in config.accounts
        assert config.accounts["test"].label == "Test"

    def test_nested_config_defaults(self) -> None:
        """Test nested config objects have defaults."""
        config = VantaGridConfig()
        assert config.switching.enabled is True
        assert config.skills.install_dir == Path("~/.claude/skills")
        assert config.hotkeys.swap_focus == "ctrl+s"
