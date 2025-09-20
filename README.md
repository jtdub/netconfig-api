# NetConfigAPI

A vendor-agnostic REST API that translates a standard REST interface into network configuration commands for multi-vendor network devices.

## Features

- 🌐 **Multi-vendor support**: Cisco IOS/NX-OS/IOS-XR, Juniper Junos, Arista EOS
- 🚀 **FastAPI**: Modern, fast web framework with automatic API documentation
- 🔒 **Type Safety**: Full type hints and validation with Pydantic
- 🧪 **Test-Driven Development**: Comprehensive test suite with 85%+ coverage
- 🐳 **Container Ready**: Docker and Docker Compose support
- 📊 **Code Quality**: Ruff, Pylint, and MyPy integration
- 📚 **Auto Documentation**: Interactive API docs with Swagger UI and ReDoc

## Quick Start

### Prerequisites

- Python 3.10-3.13
- Poetry (for dependency management)

### Installation

```bash
# Clone the repository
git clone https://github.com/jtdub/netconfig-api.git
cd netconfig-api

# Install dependencies
poetry install

# Run tests
poetry run invoke test

# Start development server
poetry run invoke dev
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run with Docker
docker build -t netconfig-api .
docker run -p 8000:8000 netconfig-api
```

## Usage

### Configure Device Hostname

```bash
curl -X POST "http://localhost:8000/api/v1/hostname" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "example-rtr",
       "device": "192.168.1.1",
       "platform": "cisco_ios"
     }'
```

**Response:**
```json
{
  "success": true,
  "message": "Hostname 'example-rtr' configured successfully on 192.168.1.1",
  "device": "192.168.1.1",
  "hostname": "example-rtr"
}
```

### Supported Platforms

| Platform | Command Generated |
|----------|-------------------|
| `cisco_ios` | `hostname {name}` |
| `cisco_nxos` | `hostname {name}` |
| `cisco_iosxr` | `hostname {name}` |
| `juniper_junos` | `set system host-name {name}` |
| `arista_eos` | `hostname {name}` |

## API Documentation

Once the server is running, visit:

- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Development

### Available Commands

```bash
# Run tests with coverage
poetry run invoke test

# Run linting
poetry run invoke lint

# Format code
poetry run invoke format-code

# Type checking
poetry run invoke type-check

# Run all quality checks
poetry run invoke check-all

# Start development server with auto-reload
poetry run invoke dev

# Build Docker image
poetry run invoke docker-build
```

### Project Structure

```
netconfig-api/
├── netconfig_api/           # Main application package
│   ├── api/                # API endpoints
│   ├── models/             # Pydantic models
│   ├── services/           # Business logic
│   ├── utils/              # Utilities
│   └── main.py             # FastAPI app
├── tests/                  # Test suite
├── docs/                   # Documentation
├── tasks.py                # Invoke tasks
├── Dockerfile              # Container definition
├── docker-compose.yml      # Multi-container setup
└── pyproject.toml          # Poetry configuration
```

### Code Quality

This project uses:

- **Ruff**: Fast linting and formatting
- **Pylint**: Additional code analysis
- **MyPy**: Static type checking
- **pytest**: Testing framework with coverage
- **Black**: Code formatting (via Ruff)

### Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=netconfig_api

# Run specific test file
poetry run pytest tests/test_main.py -v
```

## Architecture

### Request Flow

1. **API Layer** (`netconfig_api/api/`): FastAPI endpoints handle HTTP requests
2. **Model Layer** (`netconfig_api/models/`): Pydantic models validate input/output
3. **Service Layer** (`netconfig_api/services/`): Business logic for device configuration
4. **Utility Layer** (`netconfig_api/utils/`): Platform-specific command generation

### Design Patterns

- **Dependency Injection**: Services are injected into API endpoints
- **Repository Pattern**: Service layer abstracts device communication
- **Command Pattern**: Platform-specific command generation
- **Factory Pattern**: Platform validation and command template selection

## Production Considerations

This is a demonstration API. For production use, consider:

1. **Authentication & Authorization**: Add API keys, OAuth, or JWT tokens
2. **Device Communication**: Implement actual SSH/NETCONF connections
3. **Error Handling**: Add retry logic and graceful degradation
4. **Monitoring**: Add logging, metrics, and health checks
5. **Security**: Input sanitization, rate limiting, and audit trails
6. **Configuration Management**: Environment-based configuration
7. **Database**: Persistent storage for device inventory and audit logs

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests and ensure code quality (`poetry run invoke check-all`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.