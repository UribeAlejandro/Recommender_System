import pytest
from fastapi.testclient import TestClient

from backend.main import create_application


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    """
    Create a test client for the FastAPI application.

    Yields
    ------
    TestClient
        The test client
    """
    client = TestClient(create_application())
    yield client
