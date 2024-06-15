import pytest
from fastapi.testclient import TestClient
from ...endpoints.app import app


@pytest.fixture(scope="session")
def test_app():
    return TestClient(app)
