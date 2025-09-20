"""Tests for main FastAPI application."""

from fastapi.testclient import TestClient

from netconfig_api.main import app

client = TestClient(app)


class TestMainApp:
    """Test cases for main FastAPI application."""

    def test_root_endpoint(self) -> None:
        """Test root endpoint returns correct information."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == "NetConfigAPI"
        assert data["version"] == "0.1.0"
        assert "description" in data
        assert data["docs_url"] == "/docs"
        assert data["health_check"] == "/health"

    def test_health_check_endpoint(self) -> None:
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert data["service"] == "NetConfigAPI"

    def test_docs_endpoint_accessible(self) -> None:
        """Test that OpenAPI docs are accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_json_accessible(self) -> None:
        """Test that OpenAPI JSON is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        data = response.json()
        assert data["info"]["title"] == "NetConfigAPI"
        assert data["info"]["version"] == "0.1.0"
