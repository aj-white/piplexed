from unittest.mock import create_autospec
from unittest.mock import patch

import pytest
from packaging.version import Version
from pypi_simple import DistributionPackage
from pypi_simple import NoSuchProjectError
from pypi_simple.client import PyPISimple

from piplexed.pypi.pypi_info import find_most_recent_version_on_pypi
from piplexed.pypi.pypi_info import get_pypi_versions
from piplexed.pypi.pypi_info import latest_pypi_version
from piplexed.pypi.pypi_info import pypi_package_info
from piplexed.venvs.pipx_venvs import PackageInfo


@pytest.mark.parametrize(
    "packages_data, is_prerelease, expected",
    [
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0b0", "sdist", False),
            ],
            False,
            Version("1.0.0"),
            id="no pre-releases",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0b0", "sdist", False),
            ],
            True,
            Version("2.0b0"),
            id="pre-release allowed",
        ),
    ],
)
def test_get_latest_version_prerelease_flag(packages_data, is_prerelease, expected):
    packages = [
        create_autospec(DistributionPackage, version=v, package_type=t, is_yanked=y) for v, t, y in packages_data
    ]
    assert latest_pypi_version(packages, is_prerelease=is_prerelease) == expected


@pytest.mark.parametrize(
    "packages_data, is_prerelease, expected",
    [
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.5.0", "sdist", False),
            ],
            False,
            Version("2.5.0"),
            id="standard sdists",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.5.0", "sdist", True),
            ],
            False,
            Version("2.0.0"),
            id="yanked sdists",
        ),
        pytest.param(
            [
                ("2.0.0", "sdist", False),
                ("2.5.0", "sdist", False),
                ("1.0.0", "sdist", False),
            ],
            False,
            Version("2.5.0"),
            id="jumbled sdists",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.5b0", "sdist", False),
            ],
            False,
            Version("2.0.0"),
            id="pre_lease sdist",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", True),
                ("2.5b0", "sdist", False),
            ],
            False,
            Version("1.0.0"),
            id="pre_release and yanked sdists",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("invalid", "sdist", False),
            ],
            False,
            Version("1.0.0"),
            id="Invalid version does not fail",
        ),
    ],
)
def test_get_latest_version_sdists(packages_data, is_prerelease, expected):
    """
    Test examples are all sdists as piplexed only finds versions for sdists
    """
    packages = [
        create_autospec(DistributionPackage, version=v, package_type=t, is_yanked=y) for v, t, y in packages_data
    ]
    assert latest_pypi_version(packages, is_prerelease=is_prerelease) == expected


@pytest.mark.parametrize(
    "packages_data, is_prerelease, expected",
    [
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.5.0", "wheel", False),
            ],
            False,
            Version("2.0.0"),
            id="single wheel",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.0.0", "wheel", False),
            ],
            False,
            Version("2.0.0"),
            id="sdist and wheel",
        ),
        pytest.param(
            [
                ("2.0.0", "sdist", False),
                ("2.5.0", "wheel", False),
                ("1.0.0", "sdist", False),
            ],
            False,
            Version("2.0.0"),
            id="jumbled single wheel",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.5.0", "wheel", True),
            ],
            False,
            Version("2.0.0"),
            id="single yanked wheel",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", True),
                ("2.5.0", "wheel", False),
            ],
            False,
            Version("1.0.0"),
            id="single wheel yanked sdist",
        ),
    ],
)
def test_get_latest_version_wheels(packages_data, is_prerelease, expected):
    """
    Piplexed only finds versions for sdists, this test, this test ensures wheels
    aren't included.
    """
    packages = [
        create_autospec(DistributionPackage, version=v, package_type=t, is_yanked=y) for v, t, y in packages_data
    ]
    assert latest_pypi_version(packages, is_prerelease=is_prerelease) == expected


@patch("piplexed.pypi.pypi_info.pypi_package_info")
def test_get_pypi_versions(mock_page):
    pypi_packages_data = [
        ("1.0.0", "sdist", False),
        ("2.0.0", "sdist", False),
        ("2.5.0", "sdist", False),
    ]
    pypi_packages = [
        create_autospec(DistributionPackage, version=v, package_type=t, is_yanked=y) for v, t, y in pypi_packages_data
    ]

    mock_page.return_value = pypi_packages

    mock_client = create_autospec(PyPISimple, spec_set=True)
    package = PackageInfo(name="testproj", version=Version("0.5.0"), python=None, latest_pypi_version=None)

    result = get_pypi_versions(client=mock_client, package=package, is_prerelease=False)
    assert [result] == [
        PackageInfo(name="testproj", version=Version("0.5.0"), python=None, latest_pypi_version=Version("2.5.0"))
    ]


# -----------------------------------------------------
# To test find_most_recent_version_on_pypi need to mock some data


@pytest.fixture
def mocked_venvs():
    return [
        PackageInfo(name="package1", version="1.0.0"),
        PackageInfo(name="package2", version="2.0.0"),
        PackageInfo(name="nonpypi-package", version="1.5.1"),
    ]


@pytest.fixture
def mock_get_pypi_versions():
    """
    In find_most_recent_version_on_pypi get_pypi_version is called for each package
    returned from get_pipx_metadata. Use side effects to get different results
    for each package.
    """
    with patch("piplexed.pypi.pypi_info.get_pypi_versions") as mock:

        def side_effect(client, pkg, is_prerelease):  # noqa: ARG001
            if pkg.name == "package1":
                return PackageInfo(
                    name="package1", version="1.0.0", latest_pypi_version="1.1.0" if not is_prerelease else "1.2.0-beta"
                )
            elif pkg.name == "package2":
                return PackageInfo(name="package2", version="2.0.0", latest_pypi_version="2.0.0")
            else:
                raise NoSuchProjectError(project="nonpypi-package", url="mock/url")

        mock.side_effect = side_effect
        yield mock


def test_find_most_recent_version_on_pypi(mocked_venvs, mock_get_pypi_versions):
    result = find_most_recent_version_on_pypi(venvs=mocked_venvs, is_prerelease=False)
    assert len(result) == 1
    assert result[0].name == "package1"
    assert result[0].version == "1.0.0"
    assert result[0].latest_pypi_version == "1.1.0"
    assert mock_get_pypi_versions.call_count == 3


def test_find_most_recent_version_on_pypi_is_prerelease(mocked_venvs, mock_get_pypi_versions):
    result = find_most_recent_version_on_pypi(venvs=mocked_venvs, is_prerelease=True)
    assert len(result) == 1
    assert result[0].name == "package1"
    assert result[0].version == "1.0.0"
    assert result[0].latest_pypi_version == "1.2.0-beta"
    assert mock_get_pypi_versions.call_count == 3


def test_find_most_recent_version_on_pypi_no_updates(mocked_venvs, mock_get_pypi_versions):
    mock_get_pypi_versions.side_effect = lambda client, pkg, is_prerelease: (  # noqa: ARG005
        PackageInfo(name="package1", version="1.0.0", latest_pypi_version="1.0.0" if is_prerelease else "1.0.0")
        if pkg.name == "package1"
        else PackageInfo(name="package2", version="2.0.0", latest_pypi_version="2.0.0")
    )

    result = find_most_recent_version_on_pypi(venvs=mocked_venvs, is_prerelease=False)
    assert not result
    assert mock_get_pypi_versions.call_count == 3


def test_find_most_recent_version_on_pypi_unstable_no_updates(mocked_venvs, mock_get_pypi_versions):
    mock_get_pypi_versions.side_effect = lambda client, pkg, is_prerelease: (  # noqa: ARG005
        PackageInfo(name="package1", version="1.0.0", latest_pypi_version="1.0.0" if is_prerelease else "1.0.0")
        if pkg.name == "package1"
        else PackageInfo(name="package2", version="2.0.0", latest_pypi_version="2.0.0")
    )

    result = find_most_recent_version_on_pypi(venvs=mocked_venvs, is_prerelease=True)
    assert not result
    assert mock_get_pypi_versions.call_count == 3


def test_pypi_package_info_non_pypi_project():
    mock_client = create_autospec(PyPISimple, instance=True)
    mock_client.get_project_page.side_effect = NoSuchProjectError("jeff", "mock/url")
    with pytest.raises(NoSuchProjectError):
        pypi_package_info(client=mock_client, package_name="jeff")
