# NetConfig API Documentation

## Overview

NetConfig API is a vendor-agnostic REST API that provides a standardized interface for configuring network devices across multiple vendors. The API abstracts vendor-specific differences and applies network configuration commands seamlessly.

## Features

- **Multi-vendor support**: Supports Cisco IOS, Cisco NX-OS, Cisco IOS-XE, Juniper JunOS, and Arista EOS
- **Standardized interface**: Consistent REST API regardless of device vendor
- **FastAPI-based**: Modern, fast, and automatically documented API
- **Type safety**: Full Pydantic model validation
- **Containerized**: Docker support for consistent deployment

## Supported Platforms

| Platform | Status | Description |
|----------|--------|-------------|
| `cisco_ios` | ✅ Supported | Cisco IOS devices |
| `cisco_nxos` | ✅ Supported | Cisco Nexus NX-OS devices |
| `cisco_xe` | ✅ Supported | Cisco IOS-XE devices |
| `juniper_junos` | ✅ Supported | Juniper JunOS devices |
| `arista_eos` | ✅ Supported | Arista EOS devices |

## API Endpoints

### POST /hostname

Configure the hostname on a network device.

**Request Body:**
```json
{
  "name": "example-rtr",
  "device": "192.168.1.1",
  "platform": "cisco_ios",
  "credentials": {
    "username": "admin",
    "password": "secret"
  }
}
```

**Parameters:**
- `name` (string, required): The hostname to configure (1-63 characters, alphanumeric, hyphens, underscores)
- `device` (string, required): IP address of the network device (IPv4 or IPv6)
- `platform` (string, required): Network device platform (see supported platforms above)
- `credentials` (object, optional): Device authentication credentials

**Response:**
```json
{
  "success": true,
  "device": "192.168.1.1",
  "platform": "cisco_ios",
  "commands_executed": [
    "configure terminal",
    "hostname example-rtr",
    "end",
    "write memory"
  ],
  "message": "Hostname 'example-rtr' configured successfully on 192.168.1.1",
  "configured_hostname": "example-rtr",
  "execution_time": 2.5,
  "error_details": null
}
```

## Quick Start

### Using Docker

1. Build and run the development container:
```bash
docker-compose up netconfig-api-dev
```

2. Access the API at `http://localhost:8000`

3. View interactive documentation at `http://localhost:8000/docs`

### Using Poetry

1. Install dependencies:
```bash
poetry install
```

2. Run the development server:
```bash
poetry run invoke dev
```

3. Access the API at `http://localhost:8000`

## Development

### Prerequisites

- Python 3.10-3.13
- Poetry
- Docker (optional)

### Setup

1. Clone the repository
2. Install dependencies: `poetry install`
3. Run tests: `poetry run invoke test`
4. Start development server: `poetry run invoke dev`

### Available Commands

```bash
# Install dependencies
poetry run invoke install

# Run tests with coverage
poetry run invoke test

# Run linting
poetry run invoke lint

# Format code
poetry run invoke format-code

# Type checking
poetry run invoke type-check

# Run all quality checks
poetry run invoke quality

# Start development server
poetry run invoke dev

# Build package
poetry run invoke build
```

## Example Usage

### Configure Cisco IOS Hostname

```bash
curl -X POST "http://localhost:8000/hostname" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "router-01",
       "device": "192.168.1.1",
       "platform": "cisco_ios"
     }'
```

### Configure Juniper JunOS Hostname

```bash
curl -X POST "http://localhost:8000/hostname" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "juniper-01",
       "device": "192.168.1.2",
       "platform": "juniper_junos",
       "credentials": {
         "username": "admin",
         "password": "secret"
       }
     }'
```

## Error Handling

The API provides detailed error messages and follows HTTP status code conventions:

- `200 OK`: Successful configuration
- `422 Unprocessable Entity`: Invalid request parameters
- `500 Internal Server Error`: Server-side errors

## Security Considerations

1. **Credentials**: In production, use secure credential storage (environment variables, secrets management)
2. **HTTPS**: Always use HTTPS in production environments
3. **Authentication**: Implement proper API authentication for production use
4. **Network Security**: Ensure secure network connectivity to target devices

## Contributing

1. Follow the established code style (Ruff + Pylint + MyPy)
2. Write tests for new functionality
3. Update documentation as needed
4. Use conventional commit messages

## License

This project is licensed under the Apache License 2.0.