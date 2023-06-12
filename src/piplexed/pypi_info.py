from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
from typing import TypedDict
from typing import cast

from packaging.utils import NormalizedName
from packaging.utils import canonicalize_name
from packaging.version import Version
from platformdirs import user_cache_dir
from pypi_simple import DistributionPackage
from pypi_simple import PyPISimple
from requests_cache import CachedSession

from piplexed.pipx_venvs import PackageInfo
from piplexed.pipx_venvs import get_pipx_metadata
from piplexed.version import VERSION

DEFAULT_CACHE: Path = Path(user_cache_dir(appname="piplexed", version=VERSION)) / "pypi_cache.sqlite"


class PackageVersions(TypedDict):
    package: NormalizedName
    pipx: Version
    pypi: Version


def get_pypi_versions(session: CachedSession, package_name: str, *, stable: bool) -> Generator[PackageInfo, None, None]:
    with PyPISimple(session=session) as client:
        package_page = client.get_project_page(package_name)
        canonicalized_pkg_name = canonicalize_name(package_page.project)

        # use max(Version) instead of reversing order of package_page as recommended in PEP 700
        # https://peps.python.org/pep-0700/

        latest_version = get_latest_version(package_page.packages, stable=stable)

        yield PackageInfo(name=canonicalized_pkg_name, version=latest_version)


def get_latest_version(packages: list[DistributionPackage], *, stable: bool) -> Version:
    if stable:
        latest_version = max(
            pkg_vsn
            for pkg in packages
            if pkg.package_type == "sdist"
            and not (pkg_vsn := Version(cast(str, pkg.version))).is_devrelease
            and not pkg.is_yanked
            and not pkg_vsn.is_prerelease
        )
    else:
        latest_version = max(
            Version(cast(str, pkg.version)) for pkg in packages if pkg.package_type == "sdist" and not pkg.is_yanked
        )

    return latest_version


def find_outdated_packages(cache_dir: Path = DEFAULT_CACHE, *, stable: bool = True) -> list[PackageVersions]:
    updates: list[PackageVersions] = []
    venvs = get_pipx_metadata()
    session = CachedSession(cache_dir, backend="sqlite", expire_after=360)
    for pkg in venvs:
        for pypi_release in get_pypi_versions(session, pkg.name, stable=stable):
            if pypi_release.version > pkg.version:
                updates.append({"package": pkg.name, "pipx": pkg.version, "pypi": pypi_release.version})
                break

    session.remove_expired_responses()
    return updates
