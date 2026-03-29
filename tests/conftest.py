from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import create_app  # noqa: E402


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    yield app
