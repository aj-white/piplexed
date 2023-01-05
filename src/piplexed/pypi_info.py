from pypi_simple import PyPISimple
from packaging.version import Version
from packaging.utils import canonicalize_name
from requests import Session

from piplexed.pipx_venvs import PackageInfo
from piplexed.pipx_venvs import get_pipx_metadata


def get_pypi_versions(session: Session, package_name: str, stable: bool):

    with PyPISimple(session=session) as client:
        package_page = client.get_project_page(package_name)
        for pkg in package_page.packages[::-1]:
            if pkg.package_type == "sdist":
                pdata = PackageInfo(name=canonicalize_name(pkg.project), version=Version(pkg.version))
                if stable:
                    if not pdata.version.is_prerelease and not pdata.version.is_devrelease:
                        yield pdata
                else:
                    yield pdata


def find_outdated_packages(stable: bool = True):
    updates = []
    venvs = get_pipx_metadata()
    for pkg in venvs:
        for pypi_release in get_pypi_versions(Session(), pkg.name, stable):
            if pypi_release.version > pkg.version:
                updates.append({"package": pkg.name, "pipx": pkg.version, "pypi": pypi_release.version})
                break

    return updates
