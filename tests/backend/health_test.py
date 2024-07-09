from starlette.testclient import TestClient


def test_health(test_app: TestClient):
    """
    Test the health route.

    Parameters
    ----------
    test_app: TestClient
        The test client
    """
    response = test_app.get("/health")
    assert response.status_code == 200
    assert response.json() == {"health": "ok"}
