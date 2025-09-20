"""Pydantic models for API requests and responses."""

from enum import Enum

from pydantic import BaseModel, Field, IPvAnyAddress, field_validator


class NetworkPlatform(str, Enum):
    """Supported network device platforms."""

    CISCO_IOS = "cisco_ios"
    CISCO_NXOS = "cisco_nxos"
    CISCO_XE = "cisco_xe"
    JUNIPER_JUNOS = "juniper_junos"
    ARISTA_EOS = "arista_eos"


class HostnameRequest(BaseModel):
    """Request model for hostname configuration."""

    name: str = Field(
        ..., min_length=1, max_length=63, description="The hostname to configure on the device"
    )
    device: IPvAnyAddress = Field(..., description="IP address of the network device")
    platform: NetworkPlatform = Field(..., description="Network device platform")
    credentials: dict[str, str] | None = Field(
        None, description="Device credentials (username, password, etc.)"
    )

    @field_validator("name")
    @classmethod
    def validate_hostname(cls, v: str) -> str:
        """Validate hostname format."""
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError(
                "Hostname must contain only alphanumeric characters, hyphens, and underscores"
            )
        if v.startswith("-") or v.endswith("-"):
            raise ValueError("Hostname cannot start or end with a hyphen")
        return v


class ConfigurationResult(BaseModel):
    """Result of a configuration operation."""

    success: bool = Field(..., description="Whether the configuration was successful")
    device: str = Field(..., description="IP address of the configured device")
    platform: NetworkPlatform = Field(..., description="Network device platform")
    commands_executed: list[str] = Field(
        default_factory=list, description="List of commands that were executed"
    )
    message: str = Field(..., description="Human-readable result message")
    error_details: str | None = Field(None, description="Error details if the operation failed")
    execution_time: float | None = Field(
        None, description="Time taken to execute the configuration in seconds"
    )


class HostnameResponse(ConfigurationResult):
    """Response model for hostname configuration."""

    configured_hostname: str | None = Field(None, description="The hostname that was configured")
