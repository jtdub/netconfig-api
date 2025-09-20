"""Hostname configuration endpoint."""

from fastapi import APIRouter, HTTPException, status

from netconfig_api.models.requests import HostnameRequest, HostnameResponse
from netconfig_api.services.network_device import NetworkDeviceService

router = APIRouter()


@router.post(
    "/hostname",
    response_model=HostnameResponse,
    status_code=status.HTTP_200_OK,
    summary="Configure device hostname",
    description="Configure the hostname on a network device",
)
async def configure_hostname(request: HostnameRequest) -> HostnameResponse:
    """Configure hostname on a network device.

    This endpoint accepts a hostname configuration request and applies it
    to the specified network device using the appropriate vendor-specific
    commands.

    Args:
        request: Hostname configuration request containing device details

    Returns:
        HostnameResponse: Result of the hostname configuration operation

    Raises:
        HTTPException: If the request is invalid or configuration fails
    """
    service = NetworkDeviceService()

    try:
        result = await service.configure_hostname(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e
