from packaging.utils import canonicalize_name
from packaging.version import Version
from pypi_simple import DistributionPackage
from pypi_simple import PyPISimple
from requests_cache import CachedSession

from piplexed.pipx_venvs import PackageInfo
from piplexed.pipx_venvs import get_pipx_metadata


def get_pypi_versions(session: CachedSession, package_name: str, *, stable: bool):
    with PyPISimple(session=session) as client:
        package_page = client.get_project_page(package_name)
        canonicalized_pkg_name = canonicalize_name(package_page.project)

        # use max(Version) instead of reversing order of package_page as recommended in PEP 700
        # https://peps.python.org/pep-0700/

        latest_version = get_latest_version(package_page.packages, stable=stable)

        yield PackageInfo(name=canonicalized_pkg_name, version=latest_version)


def get_latest_version(packages: list[DistributionPackage], *, stable: bool):
    if stable:
        latest_version = max(
            pkg_vsn
            for pkg in packages
            if pkg.package_type == "sdist"
            and not (pkg_vsn := Version(pkg.version)).is_devrelease
            and not pkg.is_yanked
            and not pkg_vsn.is_prerelease
        )
    else:
        latest_version = max(
            Version(pkg.version) for pkg in packages if pkg.package_type == "sdist" and not pkg.is_yanked
        )

    return latest_version


def find_outdated_packages(*, stable: bool = True):
    updates = []
    venvs = get_pipx_metadata()
    session = CachedSession("pypi_cache", backend="sqlite", expire_after=360)
    for pkg in venvs:
        for pypi_release in get_pypi_versions(session, pkg.name, stable):
            if pypi_release.version > pkg.version:
                updates.append({"package": pkg.name, "pipx": pkg.version, "pypi": pypi_release.version})
                break

    session.remove_expired_responses()
    return updates
