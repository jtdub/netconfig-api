"""Invoke tasks for development workflow."""

from invoke import task


@task
def install(ctx):
    """Install dependencies using Poetry."""
    ctx.run("poetry install")


@task
def test(ctx, coverage=True):
    """Run tests with optional coverage reporting."""
    if coverage:
        ctx.run("poetry run pytest --cov=netconfig_api --cov-report=term-missing")
    else:
        ctx.run("poetry run pytest")


@task
def lint(ctx):
    """Run linting with Ruff."""
    ctx.run("poetry run ruff check .")


@task
def format_code(ctx):
    """Format code with Ruff."""
    ctx.run("poetry run ruff format .")


@task
def type_check(ctx):
    """Run type checking with MyPy."""
    ctx.run("poetry run mypy netconfig_api")


@task
def pylint_check(ctx):
    """Run pylint checks."""
    ctx.run("poetry run pylint netconfig_api")


@task
def quality(ctx):
    """Run all code quality checks."""
    lint(ctx)
    type_check(ctx)
    pylint_check(ctx)


@task
def dev(ctx):
    """Start development server."""
    ctx.run("poetry run uvicorn netconfig_api.main:app --reload --host 0.0.0.0 --port 8000")


@task
def build(ctx):
    """Build the package."""
    ctx.run("poetry build")


@task
def clean(ctx):
    """Clean build artifacts."""
    ctx.run("rm -rf dist/ build/ .coverage .pytest_cache/ .mypy_cache/ .ruff_cache/")
    ctx.run("find . -type d -name __pycache__ -delete")
    ctx.run("find . -type f -name '*.pyc' -delete")
