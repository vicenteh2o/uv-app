from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_returns_hello_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from uv 🚀"}


def test_healthz_returns_alive_status():
    """Test liveness endpoint returns 200."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readyz_returns_ready_when_all_services_healthy():
    """Test readiness endpoint returns 200 when all dependencies are healthy."""
    with patch("app.api.routes.check_readiness", new_callable=AsyncMock) as mock_check:
        mock_check.return_value = (True, {"status": "ready", "database": "healthy"})

        response = client.get("/readyz")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["database"] == "healthy"


def test_readyz_returns_503_when_database_unhealthy():
    """Test readiness endpoint returns 503 when database is unavailable."""
    with patch("app.api.routes.check_readiness", new_callable=AsyncMock) as mock_check:
        mock_check.return_value = (
            False,
            {"status": "not ready", "database": "unhealthy"},
        )

        response = client.get("/readyz")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "not ready"
        assert data["database"] == "unhealthy"
