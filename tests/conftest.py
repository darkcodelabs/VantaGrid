"""Pytest configuration and shared fixtures."""
from __future__ import annotations

import sys
from pathlib import Path

# Add src to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
