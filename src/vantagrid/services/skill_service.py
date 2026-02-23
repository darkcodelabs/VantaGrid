"""Skills registry and installation service."""
from __future__ import annotations

import json
from pathlib import Path

from vantagrid.models.skill import Skill, SkillRegistry


class SkillService:
    """Manages skills installation, discovery, and registry."""

    @staticmethod
    def get_builtins_dir() -> Path:
        """Get the bundled builtins skills directory."""
        return Path(__file__).parent.parent / "skills" / "builtins"

    def list_installed(self, install_dir: Path) -> list[Skill]:
        """Scan install directory for installed skills with SKILL.md files."""
        skills = []
        if not install_dir.exists():
            return skills

        for skill_dir in install_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skill = Skill(
                    name=skill_dir.name,
                    description="",
                    version="1.0.0",
                    source="custom",
                    installed=True,
                    install_path=skill_dir,
                )
                skills.append(skill)

        return skills

    def list_available(self) -> list[Skill]:
        """Load available skills from bundled registry.json."""
        registry_file = self.get_builtins_dir() / "registry.json"

        if not registry_file.exists():
            return []

        try:
            with open(registry_file) as f:
                data = json.load(f)
            registry = SkillRegistry.model_validate(data)
            return registry.skills
        except Exception:
            return []

    def install(self, name: str, install_dir: Path) -> Skill:
        """Install a skill from builtins to the install directory."""
        builtins = self.get_builtins_dir()
        skill_src = builtins / name

        if not skill_src.exists():
            raise ValueError(f"Skill '{name}' not found in builtins")

        install_dir.mkdir(parents=True, exist_ok=True)
        skill_dest = install_dir / name

        # Copy skill from builtins
        if skill_dest.exists():
            raise ValueError(f"Skill '{name}' already installed")

        import shutil

        shutil.copytree(skill_src, skill_dest)

        return Skill(
            name=name,
            description="",
            version="1.0.0",
            source="builtin",
            installed=True,
            install_path=skill_dest,
        )

    def uninstall(self, name: str, install_dir: Path) -> None:
        """Uninstall a skill by removing its directory."""
        skill_dir = install_dir / name

        if not skill_dir.exists():
            raise ValueError(f"Skill '{name}' not installed")

        import shutil

        shutil.rmtree(skill_dir)

    def preview(self, name: str) -> str:
        """Read and return the SKILL.md content for a skill."""
        builtins = self.get_builtins_dir()
        skill_md = builtins / name / "SKILL.md"

        if not skill_md.exists():
            raise ValueError(f"Skill '{name}' not found")

        with open(skill_md) as f:
            return f.read()
