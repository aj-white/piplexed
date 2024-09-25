from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from contextlib import ExitStack
from pathlib import Path

from packaging.version import InvalidVersion
from packaging.version import Version
from platformdirs import user_cache_path
from pypi_simple import DistributionPackage
from pypi_simple import PyPISimple
from requests_cache import CachedSession
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TaskProgressColumn
from rich.progress import TextColumn
from rich.progress import TimeRemainingColumn

from piplexed.pipx_venvs import PackageInfo
from piplexed.pipx_venvs import get_pipx_metadata
from piplexed.version import VERSION

DEFAULT_CACHE: Path = user_cache_path(appname="piplexed", version=VERSION) / "pypi_cache.sqlite"


def pypi_package_info(client: PyPISimple, package_name: str) -> list[DistributionPackage]:
    project_page = client.get_project_page(package_name)
    return project_page.packages


def latest_pypi_version(pkg_versions: list[DistributionPackage], stable: bool) -> Version:  # noqa: FBT001
    versions: list[Version] = []
    for pkg in pkg_versions:
        if pkg.version is not None and pkg.package_type == "sdist" and not pkg.is_yanked:
            try:
                pkg_vsn = Version(pkg.version)
            except InvalidVersion:
                continue
            if not pkg_vsn.is_prerelease or not stable:
                versions.append(pkg_vsn)

    # use max(Version) instead of reversing order of package_page as recommended in PEP 700
    # https://peps.python.org/pep-0700/
    return max(versions)


def get_pypi_versions(client: PyPISimple, package: PackageInfo, stable: bool) -> PackageInfo:  # noqa: FBT001
    pypi_versions: list[DistributionPackage] = pypi_package_info(client=client, package_name=package.name)

    latest_version = latest_pypi_version(pypi_versions, stable=stable)

    package.latest_pypi_version = latest_version

    return package


def find_outdated_packages(cache_dir: Path = DEFAULT_CACHE, *, stable: bool = True) -> list[PackageInfo]:
    venvs: list[PackageInfo] = get_pipx_metadata()

    with ExitStack() as stack:
        session = stack.enter_context(CachedSession(str(cache_dir), backend="sqlite", expire_after=360))
        session.cache.delete(expired=True)

        client = stack.enter_context(PyPISimple(session=session))
        progress_bar = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            transient=True,
        )

        stack.enter_context(progress_bar)
        task = progress_bar.add_task("[red]Getting PyPI version data", total=len(venvs))

        executor = stack.enter_context(ThreadPoolExecutor(max_workers=4))

        results = [executor.submit(get_pypi_versions, client, pkg, stable) for pkg in venvs]

        updates = []
        for future in as_completed(results):
            result = future.result()
            if result.newer_pypi_version():
                updates.append(result)
            progress_bar.update(task, advance=1)

    return sorted(updates, key=lambda x: x.name)
