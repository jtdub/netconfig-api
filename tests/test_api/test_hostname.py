"""Tests for hostname endpoint."""

from fastapi.testclient import TestClient

from netconfig_api.main import app

client = TestClient(app)


class TestHostnameEndpoint:
    """Test hostname configuration endpoint."""

    def test_configure_hostname_success(self):
        """Test successful hostname configuration."""
        request_data = {"name": "test-router", "device": "192.168.1.1", "platform": "cisco_ios"}

        response = client.post("/hostname", json=request_data)

        assert response.status_code == 200

        response_data = response.json()
        assert response_data["success"] is True
        assert response_data["device"] == "192.168.1.1"
        assert response_data["platform"] == "cisco_ios"
        assert response_data["configured_hostname"] == "test-router"
        assert "hostname test-router" in response_data["commands_executed"]
        assert response_data["execution_time"] is not None

    def test_configure_hostname_with_credentials(self):
        """Test hostname configuration with credentials."""
        request_data = {
            "name": "test-router",
            "device": "192.168.1.1",
            "platform": "cisco_ios",
            "credentials": {"username": "admin", "password": "secret"},
        }

        response = client.post("/hostname", json=request_data)

        assert response.status_code == 200

        response_data = response.json()
        assert response_data["success"] is True
        assert response_data["configured_hostname"] == "test-router"

    def test_configure_hostname_invalid_ip(self):
        """Test hostname configuration with invalid IP address."""
        request_data = {"name": "test-router", "device": "invalid.ip", "platform": "cisco_ios"}

        response = client.post("/hostname", json=request_data)

        assert response.status_code == 422  # Validation error

    def test_configure_hostname_invalid_platform(self):
        """Test hostname configuration with invalid platform."""
        request_data = {
            "name": "test-router",
            "device": "192.168.1.1",
            "platform": "invalid_platform",
        }

        response = client.post("/hostname", json=request_data)

        assert response.status_code == 422  # Validation error

    def test_configure_hostname_invalid_name_format(self):
        """Test hostname configuration with invalid hostname format."""
        request_data = {
            "name": "test router",  # Space not allowed
            "device": "192.168.1.1",
            "platform": "cisco_ios",
        }

        response = client.post("/hostname", json=request_data)

        assert response.status_code == 422  # Validation error

    def test_configure_hostname_empty_name(self):
        """Test hostname configuration with empty hostname."""
        request_data = {"name": "", "device": "192.168.1.1", "platform": "cisco_ios"}

        response = client.post("/hostname", json=request_data)

        assert response.status_code == 422  # Validation error

    def test_configure_hostname_long_name(self):
        """Test hostname configuration with hostname too long."""
        request_data = {
            "name": "a" * 64,  # Too long
            "device": "192.168.1.1",
            "platform": "cisco_ios",
        }

        response = client.post("/hostname", json=request_data)

        assert response.status_code == 422  # Validation error

    def test_configure_hostname_different_platforms(self):
        """Test hostname configuration with different platforms."""
        platforms = ["cisco_ios", "cisco_nxos", "cisco_xe", "juniper_junos", "arista_eos"]

        for platform in platforms:
            request_data = {
                "name": f"test-{platform.replace('_', '-')}",
                "device": "192.168.1.1",
                "platform": platform,
            }

            response = client.post("/hostname", json=request_data)

            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert response_data["platform"] == platform

    def test_configure_hostname_ipv6(self):
        """Test hostname configuration with IPv6 address."""
        request_data = {"name": "test-router", "device": "2001:db8::1", "platform": "cisco_ios"}

        response = client.post("/hostname", json=request_data)

        assert response.status_code == 200

        response_data = response.json()
        assert response_data["success"] is True
        assert response_data["device"] == "2001:db8::1"

    def test_missing_required_fields(self):
        """Test request with missing required fields."""
        # Missing name
        request_data = {"device": "192.168.1.1", "platform": "cisco_ios"}

        response = client.post("/hostname", json=request_data)
        assert response.status_code == 422

        # Missing device
        request_data = {"name": "test-router", "platform": "cisco_ios"}

        response = client.post("/hostname", json=request_data)
        assert response.status_code == 422

        # Missing platform
        request_data = {"name": "test-router", "device": "192.168.1.1"}

        response = client.post("/hostname", json=request_data)
        assert response.status_code == 422
