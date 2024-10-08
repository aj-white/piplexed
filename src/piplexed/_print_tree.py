from __future__ import annotations

from collections.abc import Iterable
from typing import cast

from rich import print as rich_print
from rich.text import Text
from rich.tree import Tree

from piplexed.pipx_venvs import PackageInfo


def print_list_tree(packages: Iterable[PackageInfo]) -> None:
    tree = Tree("Pip❎ Packages", guide_style="cyan")
    for pkg in packages:
        pkg_name = Text(
            pkg.name.title(),
            "dark_orange bold",
        )
        version_info = Text("version - ", "white").append(f"{pkg.version}", "deep_sky_blue1")
        python_info = Text("python - ", "white").append(cast(str, pkg.python), "green4")
        pkg_branch = tree.add(pkg_name)
        pkg_branch.add(version_info)
        pkg_branch.add(python_info)

    rich_print(tree)


def print_list_outdated(package_data: Iterable[PackageInfo]) -> None:
    tree = Tree("Pip❌ Outdated Packages", guide_style="cyan")
    for pkg in package_data:
        pkg_name = Text(
            pkg.name.title(),
            "bright_yellow bold",
        )

        pipx_info = Text("pipx version - ", "white").append(f"{pkg.version}", "red3")
        pypi_info = Text("PyPI version - ", "white").append(f"{pkg.latest_pypi_version}", "green1")
        if pkg.latest_pypi_version is not None and pkg.latest_pypi_version.is_prerelease:
            pypi_info.append(" ⚠", "bright_yellow")

        pkg_branch = tree.add(pkg_name)
        pkg_branch.add(pipx_info)
        pkg_branch.add(pypi_info)

    rich_print(tree)
