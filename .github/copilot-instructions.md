# Copilot Instructions for NetConfigAPI

This repository contains **NetConfigAPI**, a FastAPI application that provides a standardized REST API for configuring network devices across multiple vendors.

---

## Development Guidelines

- **Language & Stack**
  - Python 3.10–3.13
  - FastAPI + Pydantic
  - Dependency and venv management: **Poetry only**
  - Task runner: `invoke` (always run via Poetry)
  - Containerized dev environment for FastAPI and Python

- **Code Style**
  - Linters: **Ruff**, **Pylint**
  - Type checking: **MyPy**
  - All imports at the top
  - Prefer **docstrings** over inline comments
  - Clear, explicit code

- **Testing & Documentation**
  - Use **TDD**: write tests and documentation before implementation
  - Tests must cover example endpoints
  - Example:  
    `POST /hostname` with  
    ```json
    {"name": "example-rtr", "device": "192.168.1.1", "platform": "cisco_ios"}
    ```  
    should log in to the device and configure the hostname with vendor-correct syntax.

---

## Project Goals

- Provide a **singular API standard** to abstract vendor differences.
- Allow network configuration to be applied seamlessly across Cisco, Juniper, Arista, etc.
- Ensure maintainability, readability, and consistency in development.

---

## Repo Structure (suggested)

```
src/netconfigapi/      # Core app code
tests/                 # Unit and integration tests
docs/                  # API and usage documentation
tasks.py               # Invoke tasks
pyproject.toml         # Poetry config
Dockerfile             # Container definition
```

---
