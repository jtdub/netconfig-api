"""Tests for request/response models."""

import pytest
from pydantic import ValidationError

from netconfig_api.models.requests import (
    ConfigurationResult,
    HostnameRequest,
    HostnameResponse,
    NetworkPlatform,
)


class TestNetworkPlatform:
    """Test NetworkPlatform enum."""

    def test_valid_platforms(self):
        """Test that all expected platforms are available."""
        expected_platforms = {"cisco_ios", "cisco_nxos", "cisco_xe", "juniper_junos", "arista_eos"}

        actual_platforms = {platform.value for platform in NetworkPlatform}
        assert actual_platforms == expected_platforms


class TestHostnameRequest:
    """Test HostnameRequest model."""

    def test_valid_request(self):
        """Test valid hostname request."""
        request = HostnameRequest(
            name="test-router", device="192.168.1.1", platform=NetworkPlatform.CISCO_IOS
        )

        assert request.name == "test-router"
        assert str(request.device) == "192.168.1.1"
        assert request.platform == NetworkPlatform.CISCO_IOS
        assert request.credentials is None

    def test_valid_request_with_credentials(self):
        """Test valid hostname request with credentials."""
        request = HostnameRequest(
            name="test-router",
            device="192.168.1.1",
            platform=NetworkPlatform.CISCO_IOS,
            credentials={"username": "admin", "password": "secret"},
        )

        assert request.credentials == {"username": "admin", "password": "secret"}

    def test_invalid_empty_name(self):
        """Test that empty hostname is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            HostnameRequest(name="", device="192.168.1.1", platform=NetworkPlatform.CISCO_IOS)

        assert "String should have at least 1 character" in str(exc_info.value)

    def test_invalid_long_name(self):
        """Test that hostname longer than 63 characters is rejected."""
        long_name = "a" * 64
        with pytest.raises(ValidationError) as exc_info:
            HostnameRequest(
                name=long_name, device="192.168.1.1", platform=NetworkPlatform.CISCO_IOS
            )

        assert "String should have at most 63 characters" in str(exc_info.value)

    def test_invalid_hostname_format(self):
        """Test that invalid hostname formats are rejected."""
        invalid_names = [
            "test router",  # space
            "test@router",  # special character
            "-router",  # starts with hyphen
            "router-",  # ends with hyphen
            "test.router",  # dot
        ]

        for invalid_name in invalid_names:
            with pytest.raises(ValidationError):
                HostnameRequest(
                    name=invalid_name, device="192.168.1.1", platform=NetworkPlatform.CISCO_IOS
                )

    def test_valid_hostname_formats(self):
        """Test valid hostname formats."""
        valid_names = [
            "router",
            "test-router",
            "test_router",
            "router123",
            "123router",
            "test-router-123",
        ]

        for valid_name in valid_names:
            request = HostnameRequest(
                name=valid_name, device="192.168.1.1", platform=NetworkPlatform.CISCO_IOS
            )
            assert request.name == valid_name

    def test_invalid_device_ip(self):
        """Test that invalid IP addresses are rejected."""
        with pytest.raises(ValidationError):
            HostnameRequest(
                name="test-router", device="invalid.ip", platform=NetworkPlatform.CISCO_IOS
            )

    def test_ipv6_device_address(self):
        """Test that IPv6 addresses are accepted."""
        request = HostnameRequest(
            name="test-router", device="2001:db8::1", platform=NetworkPlatform.CISCO_IOS
        )

        assert str(request.device) == "2001:db8::1"


class TestConfigurationResult:
    """Test ConfigurationResult model."""

    def test_successful_result(self):
        """Test successful configuration result."""
        result = ConfigurationResult(
            success=True,
            device="192.168.1.1",
            platform=NetworkPlatform.CISCO_IOS,
            commands_executed=["hostname test-router"],
            message="Hostname configured successfully",
        )

        assert result.success is True
        assert result.device == "192.168.1.1"
        assert result.platform == NetworkPlatform.CISCO_IOS
        assert result.commands_executed == ["hostname test-router"]
        assert result.message == "Hostname configured successfully"
        assert result.error_details is None
        assert result.execution_time is None

    def test_failed_result(self):
        """Test failed configuration result."""
        result = ConfigurationResult(
            success=False,
            device="192.168.1.1",
            platform=NetworkPlatform.CISCO_IOS,
            message="Configuration failed",
            error_details="Connection timeout",
            execution_time=5.2,
        )

        assert result.success is False
        assert result.error_details == "Connection timeout"
        assert result.execution_time == 5.2


class TestHostnameResponse:
    """Test HostnameResponse model."""

    def test_successful_hostname_response(self):
        """Test successful hostname configuration response."""
        response = HostnameResponse(
            success=True,
            device="192.168.1.1",
            platform=NetworkPlatform.CISCO_IOS,
            commands_executed=["hostname test-router"],
            message="Hostname configured successfully",
            configured_hostname="test-router",
            execution_time=2.5,
        )

        assert response.success is True
        assert response.configured_hostname == "test-router"
        assert response.execution_time == 2.5
