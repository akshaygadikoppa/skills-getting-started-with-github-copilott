import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module


@pytest.fixture(autouse=False)
def client():
    """Provide a TestClient and restore in-memory activities after the test."""
    original = copy.deepcopy(app_module.activities)
    with TestClient(app_module.app) as client:
        yield client
    # restore original state
    app_module.activities = original
