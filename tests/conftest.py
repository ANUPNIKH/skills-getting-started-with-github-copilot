import os
import sys
import copy
from pathlib import Path

# Ensure src is on path so tests can import app
ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import app as application_module  # noqa: E402
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client():
    # Backup activities state
    activities = application_module.activities
    backup = copy.deepcopy(activities)
    client = TestClient(application_module.app)
    yield client
    # Restore activities to original state
    activities.clear()
    activities.update(copy.deepcopy(backup))
