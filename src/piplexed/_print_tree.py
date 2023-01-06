from typing import Iterable
from rich import print as rich_print
from rich.text import Text
from rich.tree import Tree

from piplexed.pipx_venvs import PackageInfo


def print_list_tree(packages: Iterable[PackageInfo]) -> None:
    tree = Tree("🐍 Pipx Packages", guide_style="cyan")
    for pkg in packages:

        pkg_name = Text(
            pkg.name.title(),
            "bright_yellow bold",
        )
        version_info = Text("version - ", "dim").append(f"{pkg.version}", "blue")
        python_info = Text("python - ", "white").append(pkg.python, "dark_green")
        pkg_branch = tree.add(pkg_name)
        pkg_branch.add(version_info)
        pkg_branch.add(python_info)

    rich_print(tree)
