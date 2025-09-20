# NetConfigAPI Documentation

## Overview

NetConfigAPI is a vendor-agnostic REST API that translates standard REST interface commands into network device configuration commands. It provides a unified interface for configuring multi-vendor network devices.

## Features

- **Multi-vendor support**: Cisco IOS/NX-OS/IOS-XR, Juniper Junos, Arista EOS
- **RESTful API**: Standard HTTP methods and JSON payloads
- **Input validation**: Comprehensive validation of hostnames and IP addresses
- **Type safety**: Full type hints with MyPy support
- **Container ready**: Docker and Docker Compose support
- **Comprehensive testing**: Test-driven development with high coverage
- **Code quality**: Ruff, Pylint, and MyPy integration

## Supported Platforms

| Platform | Command Template |
|----------|------------------|
| cisco_ios | `hostname {hostname}` |
| cisco_nxos | `hostname {hostname}` |
| cisco_iosxr | `hostname {hostname}` |
| juniper_junos | `set system host-name {hostname}` |
| arista_eos | `hostname {hostname}` |

## API Endpoints

### Configure Hostname

**POST** `/api/v1/hostname`

Configure hostname on a network device.

#### Request Body

```json
{
  "name": "example-rtr",
  "device": "192.168.1.1",
  "platform": "cisco_ios"
}
```

#### Parameters

- `name` (string): Hostname to set on the device
  - Must be 1-63 characters
  - Alphanumeric characters and hyphens only
  - Cannot start or end with hyphen
- `device` (string): IP address of the network device (IPv4 or IPv6)
- `platform` (string): Device platform identifier

#### Response

```json
{
  "success": true,
  "message": "Hostname 'example-rtr' configured successfully on 192.168.1.1",
  "device": "192.168.1.1",
  "hostname": "example-rtr"
}
```

#### Status Codes

- `200 OK`: Configuration completed (check `success` field for actual result)
- `422 Unprocessable Entity`: Validation error in request data
- `500 Internal Server Error`: Unexpected server error

### Health Check

**GET** `/health`

Returns API health status.

#### Response

```json
{
  "status": "healthy",
  "service": "NetConfigAPI"
}
```

### Root Information

**GET** `/`

Returns API information and documentation links.

## Examples

### Basic Hostname Configuration

```bash
curl -X POST "http://localhost:8000/api/v1/hostname" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "core-router-01",
       "device": "192.168.1.1", 
       "platform": "cisco_ios"
     }'
```

### IPv6 Device

```bash
curl -X POST "http://localhost:8000/api/v1/hostname" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "ipv6-router",
       "device": "2001:db8::1",
       "platform": "juniper_junos"
     }'
```

### Using Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/hostname",
    json={
        "name": "test-switch",
        "device": "10.0.1.100",
        "platform": "arista_eos"
    }
)

result = response.json()
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
```

## Error Handling

### Validation Errors

Invalid request data returns `422 Unprocessable Entity`:

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "String should match pattern '^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'",
      "type": "string_pattern_mismatch"
    }
  ]
}
```

### Configuration Failures

Failed configurations return `200 OK` with `success: false`:

```json
{
  "success": false,
  "message": "Unsupported platform: invalid_platform",
  "device": "192.168.1.1",
  "hostname": "test-router"
}
```

## Interactive Documentation

The API provides interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Development Notes

This is a demonstration API. In a production environment, you would need to:

1. Implement actual device connections using libraries like:
   - [Netmiko](https://github.com/ktbyers/netmiko) for SSH
   - [NAPALM](https://github.com/napalm-automation/napalm) for vendor abstraction
   - [ncclient](https://github.com/ncclient/ncclient) for NETCONF

2. Add authentication and authorization

3. Implement proper error handling for network timeouts and device failures

4. Add configuration validation and rollback capabilities

5. Implement audit logging and configuration tracking