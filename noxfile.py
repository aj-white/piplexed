import nox

PYTHON_VERSIONS = ["3.11", "3.10", "3.9", "3.8"]
PYTHON_DEFAULT_VERSION = "3.11"
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = (
    "tests",
    "lint",
)

DOC_DEPENDENCIES = "requirements/docs.txt"
TEST_DEPENDENCIES = "requirements/tests.txt"
LINT_DEPENDENCIES = "requirements/linting.txt"


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    session.run("python", "-m", "pip", "install", "-U", "pip")
    session.install(".", "-r", TEST_DEPENDENCIES)
    session.run("pytest", "tests")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def lint(session):
    session.run("python", "-m", "pip", "install", "-U", "pip")
    session.install(".", "-r", LINT_DEPENDENCIES)
    session.run("black", "src", "--check")
    session.run("ruff", ".")
    session.run("mypy", "src")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def docs(session):
    session.run("python", "-m", "pip", "install", "-U", "pip")
    session.install(".", "-r", DOC_DEPENDENCIES)
    session.run("mkdocs", "build", "--clean", "--strict")
