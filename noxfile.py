import nox

PYTHON_VERSIONS = ["3.13", "3.12", "3.11", "3.10", "3.9"]
PYTHON_DEFAULT_VERSION = "3.12"

nox.needs_version = ">=2024.3.2"
nox.options.default_venv_backend = "uv|virtualenv"

nox.options.sessions = (
    "tests",
    "coverage_report",
    "lint",
)

DOC_DEPENDENCIES = "requirements/docs.txt"
TEST_DEPENDENCIES = "requirements/tests.txt"
LINT_DEPENDENCIES = "requirements/linting.txt"


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    session.install(".", "-r", TEST_DEPENDENCIES)
    session.run("coverage", "run", "-m", "pytest", "tests")


@nox.session()
def coverage_report(session):
    session.install("coverage[toml]")

    session.run("coverage", "report", "--show-missing", "--fail-under=80")
    session.run("coverage", "erase")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def lint(session):
    session.install(".", "-r", LINT_DEPENDENCIES)
    session.run("ruff", "format", "src", "--check")
    session.run("ruff", "check", ".")
    session.run("mypy", "src")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def docs(session):
    session.install(".", "-r", DOC_DEPENDENCIES)
    session.run("mkdocs", "build", "--clean", "--strict")
