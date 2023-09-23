from __future__ import annotations

from collections.abc import Iterable


from rich import print as rich_print
from rich.table import Table
from rich.text import Text


from piplexed.pipx_venvs import PackageInfo
from piplexed.pypi_info import PackageVersions


def print_list_table(packages: Iterable[PackageInfo]) -> None:
    table = Table(title="Pip❎ Packages")
    table.add_column("Package Name", justify="right", style="dark_orange", no_wrap=True)
    table.add_column("Pipx Version", justify="right", style="deep_sky_blue1", no_wrap=True)
    table.add_column("Python Version", justify="right", style="dark_green", no_wrap=True)

    for pkg in packages:
        table.add_row(f"{pkg.name}", f"{pkg.version}", f"{pkg.python}")

    rich_print(table)


def print_outdated_table(package_data: Iterable[PackageVersions]) -> None:
    table = Table(title="Pip❌ Outdated Packages")
    table.add_column("Package Name", justify="right", style="dark_orange", no_wrap=True)
    table.add_column("Pipx Version", justify="right", style="deep_sky_blue1", no_wrap=True)
    table.add_column("PyPI Version", justify="right", style="red3", no_wrap=True)

    for pkg in package_data:
        pypi_info = Text(f"{pkg['pypi']}", "green1")
        if pkg["pypi"].is_prerelease or pkg["pypi"].is_devrelease:
            pypi_info.append(" ⚠", "bright_yellow")

        table.add_row(pkg["package"], f"{pkg['pipx']}", pypi_info)

    rich_print(table)
