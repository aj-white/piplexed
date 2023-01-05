from typing import Iterable
from packaging.version import Version
from rich import print as rich_print
from rich.text import Text
from rich.tree import Tree

from piplexed.pipx_venvs import PackageInfo

test_data = [
    PackageInfo(name="black", version=Version("22.12.0")),
    PackageInfo(name="build", version=Version("0.9.0")),
    PackageInfo(name="cookiecutter", version=Version("2.1.1")),
    PackageInfo(name="flake8", version=Version("6.0.0")),
    PackageInfo(name="hatch", version=Version("1.6.3")),
    PackageInfo(name="isort", version=Version("5.11.3")),
    PackageInfo(name="johnnydep", version=Version("1.16")),
    PackageInfo(name="mypy", version=Version("0.991")),
    PackageInfo(name="nox", version=Version("2022.11.21")),
    PackageInfo(name="pre-commit", version=Version("2.20.0")),
    PackageInfo(name="ruff", version=Version("0.0.186")),
    PackageInfo(name="tox", version=Version("4.2.3")),
    PackageInfo(name="twine", version=Version("4.0.2")),
    PackageInfo(name="virtualenv", version=Version("20.17.1")),
]


def print_tree(packages: Iterable[PackageInfo]) -> None:
    tree = Tree("🐍 Pipx Packages", guide_style="cyan")
    for pkg in packages:
        text = Text(
            pkg.name.title(),
            "bright_yellow bold",
        )
        version_info = Text("version - ", "dim").append(f"{pkg.version}", "blue")
        tree.add(text).add(version_info)

    rich_print(tree)


if __name__ == "__main__":
    print_tree(test_data)
