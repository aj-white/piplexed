from __future__ import annotations

from collections.abc import Iterable
from typing import cast

from rich import print as rich_print
from rich.text import Text
from rich.tree import Tree

from piplexed.pipx_venvs import PackageInfo
from piplexed.pypi_info import PackageVersions


def print_list_tree(packages: Iterable[PackageInfo]) -> None:
    tree = Tree("Pip❎ Packages", guide_style="cyan")
    for pkg in packages:
        pkg_name = Text(
            pkg.name.title(),
            "dark_orange bold",
        )
        version_info = Text("version - ", "white").append(f"{pkg.version}", "deep_sky_blue1")
        python_info = Text("python - ", "white").append(cast(str, pkg.python), "dark_green")
        pkg_branch = tree.add(pkg_name)
        pkg_branch.add(version_info)
        pkg_branch.add(python_info)

    rich_print(tree)


def print_list_outdated(package_data: Iterable[PackageVersions]) -> None:
    tree = Tree("Pip❌ Outdated Packages", guide_style="cyan")
    for pkg in package_data:
        pkg_name = Text(
            pkg["package"].title(),
            "bright_yellow bold",
        )

        pipx_info = Text("pipx version - ", "white").append(f"{pkg['pipx']}", "red3")
        pypi_info = Text("PyPI version - ", "white").append(f"{pkg['pypi']}", "green1")
        if pkg["pypi"].is_prerelease or pkg["pypi"].is_devrelease:
            pypi_info.append(" ⚠", "bright_yellow")

        pkg_branch = tree.add(pkg_name)
        pkg_branch.add(pipx_info)
        pkg_branch.add(pypi_info)

    rich_print(tree)
