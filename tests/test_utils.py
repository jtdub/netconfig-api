"""Tests for device platform utilities."""

import pytest

from netconfig_api.utils.device_platforms import (
    SupportedPlatform,
    get_hostname_command_template,
    get_supported_platforms,
    validate_platform,
)


class TestSupportedPlatform:
    """Test cases for SupportedPlatform enum."""

    def test_platform_values(self) -> None:
        """Test that platform enum has expected values."""
        expected_platforms = {
            "cisco_ios",
            "cisco_nxos",
            "cisco_iosxr",
            "juniper_junos",
            "arista_eos"
        }

        actual_platforms = {platform.value for platform in SupportedPlatform}
        assert actual_platforms == expected_platforms


class TestGetSupportedPlatforms:
    """Test cases for get_supported_platforms function."""

    def test_returns_list_of_strings(self) -> None:
        """Test that function returns list of platform strings."""
        platforms = get_supported_platforms()

        assert isinstance(platforms, list)
        assert all(isinstance(platform, str) for platform in platforms)
        assert len(platforms) > 0

    def test_contains_expected_platforms(self) -> None:
        """Test that returned list contains expected platforms."""
        platforms = get_supported_platforms()

        expected_platforms = [
            "cisco_ios",
            "cisco_nxos",
            "cisco_iosxr",
            "juniper_junos",
            "arista_eos"
        ]

        for platform in expected_platforms:
            assert platform in platforms


class TestValidatePlatform:
    """Test cases for validate_platform function."""

    def test_valid_platforms(self) -> None:
        """Test validation of supported platforms."""
        valid_platforms = [
            "cisco_ios",
            "cisco_nxos",
            "cisco_iosxr",
            "juniper_junos",
            "arista_eos"
        ]

        for platform in valid_platforms:
            assert validate_platform(platform) is True

    def test_invalid_platforms(self) -> None:
        """Test validation of unsupported platforms."""
        invalid_platforms = [
            "invalid_platform",
            "cisco_ios_xe",
            "juniper",
            "",
            "CISCO_IOS"  # Wrong case
        ]

        for platform in invalid_platforms:
            assert validate_platform(platform) is False


class TestGetHostnameCommandTemplate:
    """Test cases for get_hostname_command_template function."""

    def test_cisco_ios_template(self) -> None:
        """Test hostname command template for Cisco IOS."""
        template = get_hostname_command_template("cisco_ios")
        assert template == "hostname {hostname}"

    def test_cisco_nxos_template(self) -> None:
        """Test hostname command template for Cisco NX-OS."""
        template = get_hostname_command_template("cisco_nxos")
        assert template == "hostname {hostname}"

    def test_cisco_iosxr_template(self) -> None:
        """Test hostname command template for Cisco IOS-XR."""
        template = get_hostname_command_template("cisco_iosxr")
        assert template == "hostname {hostname}"

    def test_juniper_junos_template(self) -> None:
        """Test hostname command template for Juniper Junos."""
        template = get_hostname_command_template("juniper_junos")
        assert template == "set system host-name {hostname}"

    def test_arista_eos_template(self) -> None:
        """Test hostname command template for Arista EOS."""
        template = get_hostname_command_template("arista_eos")
        assert template == "hostname {hostname}"

    def test_template_formatting(self) -> None:
        """Test that template can be formatted with hostname."""
        template = get_hostname_command_template("cisco_ios")
        command = template.format(hostname="test-router")
        assert command == "hostname test-router"

    def test_unsupported_platform_raises_error(self) -> None:
        """Test that unsupported platform raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_hostname_command_template("unsupported_platform")

        assert "Unsupported platform: unsupported_platform" in str(exc_info.value)
