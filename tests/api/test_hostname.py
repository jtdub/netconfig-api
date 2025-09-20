"""Tests for hostname API endpoint."""

from fastapi.testclient import TestClient

from netconfig_api.main import app

client = TestClient(app)


class TestHostnameAPI:
    """Test cases for hostname API endpoint."""

    def test_configure_hostname_success(self) -> None:
        """Test successful hostname configuration."""
        request_data = {
            "name": "example-rtr",
            "device": "192.168.1.1",
            "platform": "cisco_ios"
        }

        response = client.post("/api/v1/hostname", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "configured successfully" in data["message"]
        assert data["device"] == "192.168.1.1"
        assert data["hostname"] == "example-rtr"

    def test_configure_hostname_ipv6(self) -> None:
        """Test hostname configuration with IPv6 address."""
        request_data = {
            "name": "ipv6-router",
            "device": "2001:db8::1",
            "platform": "juniper_junos"
        }

        response = client.post("/api/v1/hostname", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["device"] == "2001:db8::1"
        assert data["hostname"] == "ipv6-router"

    def test_configure_hostname_unsupported_platform(self) -> None:
        """Test hostname configuration with unsupported platform."""
        request_data = {
            "name": "test-router",
            "device": "192.168.1.1",
            "platform": "unsupported_platform"
        }

        response = client.post("/api/v1/hostname", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is False
        assert "Unsupported platform" in data["message"]
        assert data["device"] == "192.168.1.1"
        assert data["hostname"] == "test-router"

    def test_configure_hostname_unreachable_device(self) -> None:
        """Test hostname configuration with unreachable device."""
        request_data = {
            "name": "test-router",
            "device": "192.168.1.254",  # Simulated unreachable device
            "platform": "cisco_ios"
        }

        response = client.post("/api/v1/hostname", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is False
        assert "Failed to configure hostname" in data["message"]
        assert data["device"] == "192.168.1.254"
        assert data["hostname"] == "test-router"

    def test_configure_hostname_validation_errors(self) -> None:
        """Test hostname configuration with validation errors."""
        test_cases = [
            # Missing required fields
            {},
            # Invalid hostname (empty)
            {
                "name": "",
                "device": "192.168.1.1",
                "platform": "cisco_ios"
            },
            # Invalid hostname (too long)
            {
                "name": "a" * 64,
                "device": "192.168.1.1",
                "platform": "cisco_ios"
            },
            # Invalid hostname (special characters)
            {
                "name": "invalid_hostname!",
                "device": "192.168.1.1",
                "platform": "cisco_ios"
            },
            # Invalid IP address
            {
                "name": "test-router",
                "device": "invalid-ip",
                "platform": "cisco_ios"
            },
        ]

        for request_data in test_cases:
            response = client.post("/api/v1/hostname", json=request_data)
            assert response.status_code == 422  # Validation error

    def test_configure_hostname_all_platforms(self) -> None:
        """Test hostname configuration with all supported platforms."""
        platforms = [
            "cisco_ios",
            "cisco_nxos",
            "cisco_iosxr",
            "juniper_junos",
            "arista_eos"
        ]

        for platform in platforms:
            request_data = {
                "name": f"test-{platform.replace('_', '-')}",
                "device": "10.0.0.1",  # Internal network for success
                "platform": platform
            }

            response = client.post("/api/v1/hostname", json=request_data)

            assert response.status_code == 200, f"Failed for platform: {platform}"
            data = response.json()
            assert data["success"] is True, f"Configuration failed for platform: {platform}"

    def test_configure_hostname_request_examples(self) -> None:
        """Test the exact example from requirements."""
        request_data = {
            "name": "example-rtr",
            "device": "192.168.1.1",
            "platform": "cisco_ios"
        }

        response = client.post("/api/v1/hostname", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "success" in data
        assert "message" in data
        assert "device" in data
        assert "hostname" in data

        # Verify content
        assert data["success"] is True
        assert data["device"] == "192.168.1.1"
        assert data["hostname"] == "example-rtr"
