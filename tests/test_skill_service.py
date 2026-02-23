"""Test SkillService."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from vantagrid.models.skill import Skill, SkillRegistry
from vantagrid.services.skill_service import SkillService


class TestSkillService:
    """Test SkillService."""

    def test_list_installed_empty_dir(self, tmp_path: Path) -> None:
        """Test list_installed with empty directory."""
        service = SkillService()
        skills = service.list_installed(tmp_path)
        assert skills == []

    def test_list_installed_nonexistent_dir(self, tmp_path: Path) -> None:
        """Test list_installed with non-existent directory."""
        service = SkillService()
        nonexistent = tmp_path / "nonexistent"
        skills = service.list_installed(nonexistent)
        assert skills == []

    def test_list_installed_finds_skills(self, tmp_path: Path) -> None:
        """Test list_installed finds skills with SKILL.md."""
        service = SkillService()

        skill_dir = tmp_path / "test_skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test Skill")

        skills = service.list_installed(tmp_path)

        assert len(skills) == 1
        assert skills[0].name == "test_skill"
        assert skills[0].installed is True
        assert skills[0].source == "custom"

    def test_list_installed_ignores_dirs_without_skill_md(self, tmp_path: Path) -> None:
        """Test list_installed ignores dirs without SKILL.md."""
        service = SkillService()

        (tmp_path / "dir_without_skill").mkdir()
        skill_dir = tmp_path / "with_skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Skill")

        skills = service.list_installed(tmp_path)

        assert len(skills) == 1
        assert skills[0].name == "with_skill"

    def test_list_installed_ignores_files(self, tmp_path: Path) -> None:
        """Test list_installed ignores files."""
        service = SkillService()

        (tmp_path / "file.txt").write_text("test")
        skill_dir = tmp_path / "skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Skill")

        skills = service.list_installed(tmp_path)

        assert len(skills) == 1
        assert skills[0].name == "skill"

    def test_list_available_empty_registry(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test list_available with no registry file."""
        service = SkillService()
        monkeypatch.setattr(service, "get_builtins_dir", lambda: tmp_path)

        skills = service.list_available()
        assert skills == []

    def test_list_available_from_registry(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test list_available reads from registry.json."""
        service = SkillService()
        builtins = tmp_path / "builtins"
        builtins.mkdir()

        registry_data = {
            "skills": [
                {
                    "name": "skill1",
                    "description": "Skill 1",
                    "version": "1.0.0",
                    "source": "builtin",
                    "installed": False,
                },
                {
                    "name": "skill2",
                    "description": "Skill 2",
                    "version": "2.0.0",
                    "source": "builtin",
                    "installed": False,
                },
            ]
        }
        registry_file = builtins / "registry.json"
        registry_file.write_text(json.dumps(registry_data))

        monkeypatch.setattr(service, "get_builtins_dir", lambda: builtins)

        skills = service.list_available()
        assert len(skills) == 2
        assert skills[0].name == "skill1"
        assert skills[1].name == "skill2"

    def test_install_skill(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test install copies skill from builtins."""
        service = SkillService()
        builtins = tmp_path / "builtins"
        builtins.mkdir()
        skill_src = builtins / "test_skill"
        skill_src.mkdir()
        (skill_src / "SKILL.md").write_text("# Test")
        (skill_src / "main.py").write_text("print('test')")

        install_dir = tmp_path / "install"

        monkeypatch.setattr(service, "get_builtins_dir", lambda: builtins)

        skill = service.install("test_skill", install_dir)

        assert skill.name == "test_skill"
        assert skill.installed is True
        assert (install_dir / "test_skill" / "SKILL.md").exists()
        assert (install_dir / "test_skill" / "main.py").exists()

    def test_install_skill_not_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test install raises when skill not in builtins."""
        service = SkillService()
        builtins = tmp_path / "builtins"
        builtins.mkdir()

        monkeypatch.setattr(service, "get_builtins_dir", lambda: builtins)

        with pytest.raises(ValueError, match="not found"):
            service.install("nonexistent", tmp_path / "install")

    def test_install_already_installed(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test install raises when already installed."""
        service = SkillService()
        builtins = tmp_path / "builtins"
        builtins.mkdir()
        skill_src = builtins / "test_skill"
        skill_src.mkdir()

        install_dir = tmp_path / "install"
        install_dir.mkdir()
        (install_dir / "test_skill").mkdir()

        monkeypatch.setattr(service, "get_builtins_dir", lambda: builtins)

        with pytest.raises(ValueError, match="already installed"):
            service.install("test_skill", install_dir)

    def test_uninstall_skill(self, tmp_path: Path) -> None:
        """Test uninstall removes skill directory."""
        service = SkillService()

        install_dir = tmp_path / "install"
        install_dir.mkdir()
        skill_dir = install_dir / "test_skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test")

        assert skill_dir.exists()
        service.uninstall("test_skill", install_dir)
        assert not skill_dir.exists()

    def test_uninstall_not_found(self, tmp_path: Path) -> None:
        """Test uninstall raises when skill not installed."""
        service = SkillService()

        with pytest.raises(ValueError, match="not installed"):
            service.uninstall("nonexistent", tmp_path)

    def test_preview_skill(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test preview reads SKILL.md content."""
        service = SkillService()
        builtins = tmp_path / "builtins"
        builtins.mkdir()
        skill_dir = builtins / "test_skill"
        skill_dir.mkdir()
        skill_md_content = "# Test Skill\n\nThis is a test skill."
        (skill_dir / "SKILL.md").write_text(skill_md_content)

        monkeypatch.setattr(service, "get_builtins_dir", lambda: builtins)

        content = service.preview("test_skill")
        assert content == skill_md_content

    def test_preview_not_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test preview raises when skill not found."""
        service = SkillService()
        builtins = tmp_path / "builtins"
        builtins.mkdir()

        monkeypatch.setattr(service, "get_builtins_dir", lambda: builtins)

        with pytest.raises(ValueError, match="not found"):
            service.preview("nonexistent")

    def test_get_builtins_dir(self) -> None:
        """Test get_builtins_dir returns correct path."""
        service = SkillService()
        builtins_dir = service.get_builtins_dir()

        assert builtins_dir.name == "builtins"
        assert "skills" in str(builtins_dir)
