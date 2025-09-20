"""Invoke tasks for NetConfigAPI development."""

from invoke import task


@task
def test(ctx):
    """Run all tests with coverage."""
    ctx.run("poetry run python -m pytest tests/ -v --cov=netconfig_api --cov-report=term-missing")


@task
def test_fast(ctx):
    """Run tests without coverage for faster feedback."""
    ctx.run("poetry run python -m pytest tests/ -v")


@task
def lint(ctx):
    """Run linting with ruff."""
    ctx.run("poetry run ruff check netconfig_api tests")


@task
def format_code(ctx):
    """Format code with ruff and black."""
    ctx.run("poetry run ruff format netconfig_api tests")
    ctx.run("poetry run black netconfig_api tests")


@task
def type_check(ctx):
    """Run type checking with mypy."""
    ctx.run("poetry run mypy netconfig_api")


@task
def pylint_check(ctx):
    """Run pylint checks."""
    ctx.run("poetry run pylint netconfig_api")


@task
def check_all(ctx):
    """Run all code quality checks."""
    print("Running linting...")
    lint(ctx)
    print("\nRunning type checking...")
    type_check(ctx)
    print("\nRunning pylint...")
    pylint_check(ctx)
    print("\nRunning tests...")
    test(ctx)


@task
def dev(ctx):
    """Start development server."""
    ctx.run("poetry run uvicorn netconfig_api.main:app --reload --host 0.0.0.0 --port 8000")


@task
def serve(ctx):
    """Start production server."""
    ctx.run("poetry run uvicorn netconfig_api.main:app --host 0.0.0.0 --port 8000")


@task
def docs(ctx):
    """Open API documentation in browser."""
    import webbrowser
    webbrowser.open("http://localhost:8000/docs")


@task
def clean(ctx):
    """Clean up generated files."""
    ctx.run("rm -rf .pytest_cache")
    ctx.run("rm -rf htmlcov")
    ctx.run("rm -rf .coverage")
    ctx.run("rm -rf .mypy_cache")
    ctx.run("rm -rf .ruff_cache")
    ctx.run("find . -type d -name __pycache__ -exec rm -rf {} +", warn=True)


@task
def install(ctx):
    """Install dependencies."""
    ctx.run("poetry install")


@task
def update(ctx):
    """Update dependencies."""
    ctx.run("poetry update")


@task
def build(ctx):
    """Build the package."""
    ctx.run("poetry build")


@task
def docker_build(ctx):
    """Build Docker image."""
    ctx.run("docker build -t netconfig-api .")


@task
def docker_run(ctx):
    """Run Docker container."""
    ctx.run("docker run -p 8000:8000 netconfig-api")


@task
def docker_dev(ctx):
    """Run Docker container in development mode."""
    ctx.run("docker-compose up --build")


@task
def setup(ctx):
    """Setup development environment."""
    print("Setting up development environment...")
    install(ctx)
    print("Running initial tests...")
    test_fast(ctx)
    print("Setup complete!")