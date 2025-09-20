"""Tests for network configuration service."""

import pytest

from netconfig_api.models.requests import HostnameRequest, HostnameResponse
from netconfig_api.services.network_config import NetworkConfigService


class TestNetworkConfigService:
    """Test cases for NetworkConfigService."""

    @pytest.fixture
    def service(self) -> NetworkConfigService:
        """Create a NetworkConfigService instance for testing."""
        return NetworkConfigService()

    @pytest.mark.asyncio
    async def test_configure_hostname_success(self, service: NetworkConfigService) -> None:
        """Test successful hostname configuration."""
        request = HostnameRequest(
            name="test-router",
            device="192.168.1.1",
            platform="cisco_ios"
        )

        response = await service.configure_hostname(request)

        assert isinstance(response, HostnameResponse)
        assert response.success is True
        assert "configured successfully" in response.message
        assert response.device == "192.168.1.1"
        assert response.hostname == "test-router"

    @pytest.mark.asyncio
    async def test_configure_hostname_unsupported_platform(
        self,
        service: NetworkConfigService
    ) -> None:
        """Test hostname configuration with unsupported platform."""
        request = HostnameRequest(
            name="test-router",
            device="192.168.1.1",
            platform="unsupported_platform"
        )

        response = await service.configure_hostname(request)

        assert isinstance(response, HostnameResponse)
        assert response.success is False
        assert "Unsupported platform" in response.message
        assert response.device == "192.168.1.1"
        assert response.hostname == "test-router"

    @pytest.mark.asyncio
    async def test_configure_hostname_device_unreachable(
        self,
        service: NetworkConfigService
    ) -> None:
        """Test hostname configuration with unreachable device."""
        request = HostnameRequest(
            name="test-router",
            device="192.168.1.254",  # This will simulate failure
            platform="cisco_ios"
        )

        response = await service.configure_hostname(request)

        assert isinstance(response, HostnameResponse)
        assert response.success is False
        assert "Failed to configure hostname" in response.message
        assert response.device == "192.168.1.254"
        assert response.hostname == "test-router"

    @pytest.mark.asyncio
    async def test_configure_hostname_all_platforms(
        self,
        service: NetworkConfigService
    ) -> None:
        """Test hostname configuration with all supported platforms."""
        platforms = [
            "cisco_ios",
            "cisco_nxos",
            "cisco_iosxr",
            "juniper_junos",
            "arista_eos"
        ]

        for platform in platforms:
            request = HostnameRequest(
                name=f"test-{platform.replace('_', '-')}",
                device="10.0.0.1",  # Internal network for success
                platform=platform
            )

            response = await service.configure_hostname(request)

            assert isinstance(response, HostnameResponse)
            assert response.success is True, f"Failed for platform: {platform}"
            assert response.device == "10.0.0.1"

    @pytest.mark.asyncio
    async def test_simulate_device_configuration_success(
        self,
        service: NetworkConfigService
    ) -> None:
        """Test device configuration simulation success."""
        result = await service._simulate_device_configuration(
            device_ip="192.168.1.1",
            command="hostname test-router",
            platform="cisco_ios"
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_simulate_device_configuration_failure(
        self,
        service: NetworkConfigService
    ) -> None:
        """Test device configuration simulation failure."""
        result = await service._simulate_device_configuration(
            device_ip="192.168.1.254",
            command="hostname test-router",
            platform="cisco_ios"
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_simulate_device_configuration_internal_network(
        self,
        service: NetworkConfigService
    ) -> None:
        """Test device configuration simulation with internal network."""
        result = await service._simulate_device_configuration(
            device_ip="10.1.1.1",
            command="hostname test-router",
            platform="cisco_ios"
        )

        assert result is True
