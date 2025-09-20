"""Tests for request and response models."""

import pytest
from pydantic import ValidationError

from netconfig_api.models.requests import HostnameRequest, HostnameResponse


class TestHostnameRequest:
    """Test cases for HostnameRequest model."""

    def test_valid_hostname_request(self) -> None:
        """Test valid hostname request creation."""
        request_data = {
            "name": "example-rtr",
            "device": "192.168.1.1",
            "platform": "cisco_ios"
        }

        request = HostnameRequest(**request_data)

        assert request.name == "example-rtr"
        assert str(request.device) == "192.168.1.1"
        assert request.platform == "cisco_ios"

    def test_ipv6_device_address(self) -> None:
        """Test hostname request with IPv6 device address."""
        request_data = {
            "name": "ipv6-rtr",
            "device": "2001:db8::1",
            "platform": "cisco_ios"
        }

        request = HostnameRequest(**request_data)
        assert str(request.device) == "2001:db8::1"

    def test_invalid_hostname_empty(self) -> None:
        """Test hostname request with empty name."""
        request_data = {
            "name": "",
            "device": "192.168.1.1",
            "platform": "cisco_ios"
        }

        with pytest.raises(ValidationError) as exc_info:
            HostnameRequest(**request_data)

        assert "at least 1 character" in str(exc_info.value)

    def test_invalid_hostname_too_long(self) -> None:
        """Test hostname request with name too long."""
        request_data = {
            "name": "a" * 64,  # Too long
            "device": "192.168.1.1",
            "platform": "cisco_ios"
        }

        with pytest.raises(ValidationError) as exc_info:
            HostnameRequest(**request_data)

        assert "at most 63 characters" in str(exc_info.value)

    def test_invalid_hostname_pattern(self) -> None:
        """Test hostname request with invalid characters."""
        request_data = {
            "name": "invalid_hostname!",
            "device": "192.168.1.1",
            "platform": "cisco_ios"
        }

        with pytest.raises(ValidationError) as exc_info:
            HostnameRequest(**request_data)

        assert "String should match pattern" in str(exc_info.value)

    def test_invalid_device_ip(self) -> None:
        """Test hostname request with invalid IP address."""
        request_data = {
            "name": "test-rtr",
            "device": "invalid-ip",
            "platform": "cisco_ios"
        }

        with pytest.raises(ValidationError) as exc_info:
            HostnameRequest(**request_data)

        assert "value is not a valid IPv4 or IPv6 address" in str(exc_info.value)

    def test_missing_required_fields(self) -> None:
        """Test hostname request with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            HostnameRequest()

        errors = exc_info.value.errors()
        assert len(errors) == 3  # name, device, platform

        error_fields = {error["loc"][0] for error in errors}
        assert error_fields == {"name", "device", "platform"}


class TestHostnameResponse:
    """Test cases for HostnameResponse model."""

    def test_valid_hostname_response(self) -> None:
        """Test valid hostname response creation."""
        response_data = {
            "success": True,
            "message": "Hostname configured successfully",
            "device": "192.168.1.1",
            "hostname": "example-rtr"
        }

        response = HostnameResponse(**response_data)

        assert response.success is True
        assert response.message == "Hostname configured successfully"
        assert response.device == "192.168.1.1"
        assert response.hostname == "example-rtr"

    def test_error_hostname_response(self) -> None:
        """Test error hostname response creation."""
        response_data = {
            "success": False,
            "message": "Failed to connect to device",
            "device": "192.168.1.1",
            "hostname": "example-rtr"
        }

        response = HostnameResponse(**response_data)

        assert response.success is False
        assert response.message == "Failed to connect to device"
