from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from contextlib import ExitStack

from packaging.version import InvalidVersion
from packaging.version import Version
from pypi_simple import DistributionPackage
from pypi_simple import NoSuchProjectError
from pypi_simple import PyPISimple
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TaskProgressColumn
from rich.progress import TextColumn
from rich.progress import TimeRemainingColumn

from piplexed.venvs import PackageInfo


def pypi_package_info(client: PyPISimple, package_name: str) -> list[DistributionPackage]:
    """List of installable packages from PyPI for a given project"""
    project_page = client.get_project_page(package_name)
    return project_page.packages


def latest_pypi_version(pkg_versions: list[DistributionPackage], is_prerelease: bool) -> Version:  # noqa: FBT001
    """Finds most recent package version that has an sdist distribution"""
    versions: list[Version] = []
    for pkg in pkg_versions:
        if pkg.version is not None and pkg.package_type == "sdist" and not pkg.is_yanked:
            try:
                pkg_vsn = Version(pkg.version)
            except InvalidVersion:
                continue
            if not pkg_vsn.is_prerelease or is_prerelease:
                versions.append(pkg_vsn)

    # use max(Version) instead of reversing order of package_page as recommended in PEP 700
    # https://peps.python.org/pep-0700/
    return max(versions)


def get_pypi_versions(client: PyPISimple, package: PackageInfo, is_prerelease: bool) -> PackageInfo:  # noqa: FBT001
    """Update a PackageInfo dataclass with the most recent version available on PyPI"""
    pypi_versions: list[DistributionPackage] = pypi_package_info(client=client, package_name=package.name)

    latest_version = latest_pypi_version(pypi_versions, is_prerelease=is_prerelease)

    package.latest_pypi_version = latest_version

    return package


def find_most_recent_version_on_pypi(*, venvs: list[PackageInfo], is_prerelease: bool) -> list[PackageInfo]:
    """Get most recent version on PyPI for a given list of packages (PackageInfo dataclasses)"""
    with ExitStack() as stack:
        client = stack.enter_context(PyPISimple())
        progress_bar = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            transient=True,
        )

        stack.enter_context(progress_bar)
        task = progress_bar.add_task("[red]Getting PyPI version data", total=len(venvs))

        executor = stack.enter_context(ThreadPoolExecutor(max_workers=5))

        results = [executor.submit(get_pypi_versions, client, pkg, is_prerelease) for pkg in venvs]

        updates = []
        for future in as_completed(results):
            try:
                result = future.result()
            except NoSuchProjectError:
                continue

            if result.newer_pypi_version():
                updates.append(result)
            progress_bar.update(task, advance=1)

    return sorted(updates, key=lambda x: x.name)
