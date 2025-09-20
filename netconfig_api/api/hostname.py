"""Hostname configuration API endpoint."""

import logging

from fastapi import APIRouter, HTTPException, status

from netconfig_api.models.requests import HostnameRequest, HostnameResponse
from netconfig_api.services.network_config import NetworkConfigService

logger = logging.getLogger(__name__)

router = APIRouter()
service = NetworkConfigService()


@router.post(
    "/hostname",
    response_model=HostnameResponse,
    status_code=status.HTTP_200_OK,
    summary="Configure device hostname",
    description="Configure hostname on a network device",
    responses={
        200: {
            "description": "Hostname configuration result",
            "model": HostnameResponse
        },
        400: {
            "description": "Invalid request data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid hostname format"
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "name"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Internal server error"
                    }
                }
            }
        }
    }
)
async def configure_hostname(request: HostnameRequest) -> HostnameResponse:
    """Configure hostname on a network device.

    Args:
        request: Hostname configuration request containing:
            - name: Hostname to set (1-63 chars, alphanumeric and hyphens)
            - device: IP address of the network device
            - platform: Device platform (cisco_ios, juniper_junos, etc.)

    Returns:
        HostnameResponse with configuration result

    Raises:
        HTTPException: For various error conditions
    """
    logger.info(
        "Received hostname configuration request for device %s",
        request.device
    )

    try:
        response = await service.configure_hostname(request)

        # Log the result
        if response.success:
            logger.info(
                "Successfully configured hostname '%s' on device %s",
                request.name,
                request.device
            )
        else:
            logger.warning(
                "Failed to configure hostname '%s' on device %s: %s",
                request.name,
                request.device,
                response.message
            )

        return response

    except ValueError as e:
        # Handle validation errors from the service
        logger.error("Validation error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as e:
        # Handle unexpected errors
        logger.exception("Unexpected error configuring hostname: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) from e
