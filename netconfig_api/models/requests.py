"""Request and response models for the NetConfigAPI."""

from pydantic import BaseModel, Field, IPvAnyAddress


class HostnameRequest(BaseModel):
    """Request model for setting device hostname."""

    name: str = Field(
        ...,
        description="The hostname to set on the device",
        min_length=1,
        max_length=63,
        pattern=r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$"
    )
    device: IPvAnyAddress = Field(
        ...,
        description="IP address of the network device"
    )
    platform: str = Field(
        ...,
        description="Network device platform (e.g., cisco_ios, juniper_junos)"
    )


class HostnameResponse(BaseModel):
    """Response model for hostname configuration."""

    success: bool = Field(
        ...,
        description="Whether the hostname configuration was successful"
    )
    message: str = Field(
        ...,
        description="Status message describing the result"
    )
    device: str = Field(
        ...,
        description="IP address of the configured device"
    )
    hostname: str = Field(
        ...,
        description="The hostname that was configured"
    )
