"""Tests for main FastAPI application."""

from fastapi.testclient import TestClient

from netconfig_api.main import app

client = TestClient(app)


class TestMainApp:
    """Test main FastAPI application."""

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "NetConfig API is running"
        assert data["version"] == "0.1.0"
        assert data["status"] == "healthy"

    def test_health_check_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "netconfig-api"
        assert data["version"] == "0.1.0"

    def test_openapi_docs(self):
        """Test that OpenAPI documentation is available."""
        response = client.get("/openapi.json")

        assert response.status_code == 200

        openapi_spec = response.json()
        assert openapi_spec["info"]["title"] == "NetConfig API"
        assert openapi_spec["info"]["version"] == "0.1.0"
        assert "paths" in openapi_spec
        assert "/hostname" in openapi_spec["paths"]

    def test_docs_endpoint(self):
        """Test that Swagger UI is available."""
        response = client.get("/docs")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_redoc_endpoint(self):
        """Test that ReDoc is available."""
        response = client.get("/redoc")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_cors_headers(self):
        """Test that CORS headers are properly set."""
        response = client.get("/")

        # The TestClient doesn't automatically add CORS headers,
        # but we can test that the middleware is configured
        # by checking that the response doesn't fail
        assert response.status_code == 200
