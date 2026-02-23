"""Skill browser widget for browsing and managing skills."""
from __future__ import annotations

from textual.widgets import Static, Button
from textual.containers import Vertical, Horizontal
from textual.message import Message


class SkillBrowser(Vertical):
    """Panel for browsing installed and available skills."""

    class SkillSelected(Message):
        """Posted when a skill is selected."""

        def __init__(self, skill_name: str):
            super().__init__()
            self.skill_name = skill_name

    class SkillInstalled(Message):
        """Posted when a skill is installed."""

        def __init__(self, skill_name: str):
            super().__init__()
            self.skill_name = skill_name

    class SkillUninstalled(Message):
        """Posted when a skill is uninstalled."""

        def __init__(self, skill_name: str):
            super().__init__()
            self.skill_name = skill_name

    DEFAULT_CSS = """
    SkillBrowser {
        height: 1fr;
        border: round $primary;
        overflow: auto;
    }

    .skill-section-title {
        height: 1;
        background: $boost;
        color: $text;
        text-style: bold;
        padding: 0 1;
    }

    .skill-item {
        height: 3;
        border: round $panel;
        padding: 1;
        margin: 0 0 1 0;
    }

    .skill-name {
        height: 1;
        color: $accent;
        text-style: bold;
    }

    .skill-description {
        height: 1;
        color: $text-muted;
        width: 1fr;
    }

    .skill-button {
        height: 1;
        width: 1fr;
    }

    Button {
        margin-right: 1;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.installed_skills: dict[str, str] = {}  # name -> description
        self.available_skills: dict[str, str] = {}  # name -> description

    def compose(self):
        """Compose the skill browser."""
        yield Static("INSTALLED SKILLS", classes="skill-section-title")
        yield Static("", id="installed-skills-container")
        yield Static("AVAILABLE SKILLS", classes="skill-section-title")
        yield Static("", id="available-skills-container")

    def add_installed_skill(self, name: str, description: str = ""):
        """Add an installed skill to the list.

        Args:
            name: Skill name
            description: Skill description
        """
        self.installed_skills[name] = description
        self._render_skills()

    def add_available_skill(self, name: str, description: str = ""):
        """Add an available skill to the list.

        Args:
            name: Skill name
            description: Skill description
        """
        self.available_skills[name] = description
        self._render_skills()

    def _render_skills(self):
        """Re-render the skill lists."""
        self.query("Horizontal").remove()

        # Render installed skills
        for name, desc in self.installed_skills.items():
            row = Horizontal(
                Static(name, classes="skill-name"),
                Static(desc, classes="skill-description"),
                Button("Preview", id=f"skill-preview-{name}"),
                Button("Uninstall", id=f"skill-uninstall-{name}"),
                classes="skill-item",
            )
            self.mount(row)

        # Render available skills
        for name, desc in self.available_skills.items():
            row = Horizontal(
                Static(name, classes="skill-name"),
                Static(desc, classes="skill-description"),
                Button("Install", id=f"skill-install-{name}"),
                classes="skill-item",
            )
            self.mount(row)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        button_id = event.button.id
        if not button_id:
            return

        if button_id.startswith("skill-install-"):
            skill_name = button_id[14:]
            self.post_message(self.SkillInstalled(skill_name))
        elif button_id.startswith("skill-uninstall-"):
            skill_name = button_id[16:]
            self.post_message(self.SkillUninstalled(skill_name))
        elif button_id.startswith("skill-preview-"):
            skill_name = button_id[14:]
            self.post_message(self.SkillSelected(skill_name))
