"""Platform adapters for different network device vendors."""

from abc import ABC, abstractmethod

from netconfig_api.models.requests import NetworkPlatform


class PlatformAdapter(ABC):
    """Abstract base class for platform-specific adapters."""

    @abstractmethod
    def generate_hostname_commands(self, hostname: str) -> list[str]:
        """Generate platform-specific commands to set hostname."""
        pass

    @abstractmethod
    def validate_hostname(self, hostname: str) -> bool:
        """Validate hostname for platform-specific requirements."""
        pass


class CiscoIOSAdapter(PlatformAdapter):
    """Cisco IOS platform adapter."""

    def generate_hostname_commands(self, hostname: str) -> list[str]:
        """Generate Cisco IOS commands to set hostname."""
        return ["configure terminal", f"hostname {hostname}", "end", "write memory"]

    def validate_hostname(self, hostname: str) -> bool:
        """Validate hostname for Cisco IOS requirements."""
        # Cisco IOS hostname validation
        if len(hostname) > 63:
            return False
        if not hostname.replace("-", "").replace("_", "").isalnum():
            return False
        if hostname.startswith("-") or hostname.endswith("-"):
            return False
        return True


class CiscoNXOSAdapter(PlatformAdapter):
    """Cisco NX-OS platform adapter."""

    def generate_hostname_commands(self, hostname: str) -> list[str]:
        """Generate Cisco NX-OS commands to set hostname."""
        return [
            "configure terminal",
            f"hostname {hostname}",
            "exit",
            "copy running-config startup-config",
        ]

    def validate_hostname(self, hostname: str) -> bool:
        """Validate hostname for Cisco NX-OS requirements."""
        # Similar to IOS but may have slight differences
        if len(hostname) > 63:
            return False
        if not hostname.replace("-", "").replace("_", "").isalnum():
            return False
        if hostname.startswith("-") or hostname.endswith("-"):
            return False
        return True


class CiscoXEAdapter(PlatformAdapter):
    """Cisco IOS-XE platform adapter."""

    def generate_hostname_commands(self, hostname: str) -> list[str]:
        """Generate Cisco IOS-XE commands to set hostname."""
        return ["configure terminal", f"hostname {hostname}", "end", "write memory"]

    def validate_hostname(self, hostname: str) -> bool:
        """Validate hostname for Cisco IOS-XE requirements."""
        # Similar to IOS
        if len(hostname) > 63:
            return False
        if not hostname.replace("-", "").replace("_", "").isalnum():
            return False
        if hostname.startswith("-") or hostname.endswith("-"):
            return False
        return True


class JuniperJunOSAdapter(PlatformAdapter):
    """Juniper JunOS platform adapter."""

    def generate_hostname_commands(self, hostname: str) -> list[str]:
        """Generate Juniper JunOS commands to set hostname."""
        return ["configure", f"set system host-name {hostname}", "commit", "exit"]

    def validate_hostname(self, hostname: str) -> bool:
        """Validate hostname for Juniper JunOS requirements."""
        if len(hostname) > 63:
            return False
        if not hostname.replace("-", "").replace("_", "").isalnum():
            return False
        if hostname.startswith("-") or hostname.endswith("-"):
            return False
        return True


class AristaEOSAdapter(PlatformAdapter):
    """Arista EOS platform adapter."""

    def generate_hostname_commands(self, hostname: str) -> list[str]:
        """Generate Arista EOS commands to set hostname."""
        return ["configure", f"hostname {hostname}", "exit", "write memory"]

    def validate_hostname(self, hostname: str) -> bool:
        """Validate hostname for Arista EOS requirements."""
        if len(hostname) > 63:
            return False
        if not hostname.replace("-", "").replace("_", "").isalnum():
            return False
        if hostname.startswith("-") or hostname.endswith("-"):
            return False
        return True


class PlatformAdapterFactory:
    """Factory for creating platform adapters."""

    _adapters: dict[NetworkPlatform, PlatformAdapter] = {
        NetworkPlatform.CISCO_IOS: CiscoIOSAdapter(),
        NetworkPlatform.CISCO_NXOS: CiscoNXOSAdapter(),
        NetworkPlatform.CISCO_XE: CiscoXEAdapter(),
        NetworkPlatform.JUNIPER_JUNOS: JuniperJunOSAdapter(),
        NetworkPlatform.ARISTA_EOS: AristaEOSAdapter(),
    }

    @classmethod
    def get_adapter(cls, platform: NetworkPlatform) -> PlatformAdapter:
        """Get the appropriate adapter for the specified platform."""
        adapter = cls._adapters.get(platform)
        if not adapter:
            raise ValueError(f"Unsupported platform: {platform}")
        return adapter
