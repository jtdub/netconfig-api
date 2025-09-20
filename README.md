# NetConfig API

A vendor-agnostic FastAPI application that provides a standardized REST interface for configuring network devices across multiple vendors.

## 🚀 Features

- **Multi-vendor support**: Cisco IOS/NX-OS/XE, Juniper JunOS, Arista EOS
- **Standardized REST API**: Consistent interface regardless of device vendor
- **FastAPI-based**: Modern, fast, automatically documented API
- **Type safety**: Full Pydantic model validation
- **Containerized**: Docker support for consistent deployment
- **TDD approach**: Comprehensive test coverage
- **Code quality**: Ruff + Pylint + MyPy enforcement

## 🛠️ Tech Stack

- **Framework**: FastAPI + Pydantic
- **Python**: 3.10-3.13 support
- **Dependency Management**: Poetry
- **Task Runner**: Invoke
- **Code Quality**: Ruff, Pylint, MyPy
- **Testing**: pytest with async support
- **Containerization**: Docker + Docker Compose

## 📦 Quick Start

### Using Docker

```bash
# Development environment
docker-compose up netconfig-api-dev

# Production environment
docker-compose up netconfig-api-prod
```

### Using Poetry

```bash
# Install dependencies
poetry install

# Start development server
poetry run invoke dev

# Run tests
poetry run invoke test

# Run all quality checks
poetry run invoke quality
```

## 🔗 API Example

Configure a hostname on a Cisco IOS device:

```bash
curl -X POST "http://localhost:8000/hostname" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "example-rtr",
       "device": "192.168.1.1",
       "platform": "cisco_ios"
     }'
```

Response:
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
  "message": "Hostname 'example-rtr' configured successfully",
  "configured_hostname": "example-rtr",
  "execution_time": 2.5
}
```

## 📚 Documentation

- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`
- Detailed documentation: [docs/api.md](docs/api.md)

## 🧪 Development

```bash
# Setup development environment
poetry install

# Available invoke commands
poetry run invoke --list

# Run tests with coverage
poetry run invoke test

# Code formatting and linting
poetry run invoke format-code
poetry run invoke lint

# Type checking
poetry run invoke type-check

# All quality checks
poetry run invoke quality
```

## 🏗️ Project Structure

```
netconfig-api/
├── netconfig_api/          # Main application package
│   ├── api/                # API endpoints
│   ├── models/             # Pydantic models
│   ├── services/           # Business logic
│   ├── utils/              # Utilities and adapters
│   └── main.py             # FastAPI application
├── tests/                  # Test suite
├── docs/                   # Documentation
├── Dockerfile              # Container definition
├── docker-compose.yml      # Container orchestration
├── pyproject.toml          # Project configuration
└── tasks.py                # Invoke task definitions
```

## 🤝 Contributing

1. Follow TDD approach - tests first!
2. Use the established code style (enforced by tools)
3. All imports at the top
4. Prefer docstrings over inline comments
5. Clear, explicit code

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.
