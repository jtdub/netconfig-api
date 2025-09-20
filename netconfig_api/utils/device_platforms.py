"""Device platform utilities."""

from enum import Enum


class SupportedPlatform(str, Enum):
    """Supported network device platforms."""

    CISCO_IOS = "cisco_ios"
    CISCO_NXOS = "cisco_nxos"
    CISCO_IOSXR = "cisco_iosxr"
    JUNIPER_JUNOS = "juniper_junos"
    ARISTA_EOS = "arista_eos"


def get_supported_platforms() -> list[str]:
    """Get list of supported platform strings."""
    return [platform.value for platform in SupportedPlatform]


def validate_platform(platform: str) -> bool:
    """Validate if platform is supported."""
    return platform in get_supported_platforms()


def get_hostname_command_template(platform: str) -> str:
    """Get hostname configuration command template for platform."""
    command_templates: dict[str, str] = {
        SupportedPlatform.CISCO_IOS: "hostname {hostname}",
        SupportedPlatform.CISCO_NXOS: "hostname {hostname}",
        SupportedPlatform.CISCO_IOSXR: "hostname {hostname}",
        SupportedPlatform.JUNIPER_JUNOS: "set system host-name {hostname}",
        SupportedPlatform.ARISTA_EOS: "hostname {hostname}",
    }

    if platform not in command_templates:
        raise ValueError(f"Unsupported platform: {platform}")

    return command_templates[platform]
