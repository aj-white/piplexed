from unittest.mock import create_autospec
from unittest.mock import patch

import pytest
from packaging.version import Version
from pypi_simple import DistributionPackage
from pypi_simple.client import PyPISimple

from piplexed.pipx_venvs import PackageInfo
from piplexed.pypi_info import find_outdated_packages
from piplexed.pypi_info import get_pypi_versions
from piplexed.pypi_info import latest_pypi_version


@pytest.mark.parametrize(
    "packages_data, non_pre_release, expected",
    [
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0b0", "sdist", False),
            ],
            True,
            Version("1.0.0"),
            id="no pre-releases",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0b0", "sdist", False),
            ],
            False,
            Version("2.0b0"),
            id="pre-release allowed",
        ),
    ],
)
def test_get_latest_version_stable_flag(packages_data, non_pre_release, expected):
    packages = [
        create_autospec(DistributionPackage, version=v, package_type=t, is_yanked=y) for v, t, y in packages_data
    ]
    assert latest_pypi_version(packages, stable=non_pre_release) == expected


@pytest.mark.parametrize(
    "packages_data, non_pre_release, expected",
    [
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.5.0", "sdist", False),
            ],
            True,
            Version("2.5.0"),
            id="standard sdists",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.5.0", "sdist", True),
            ],
            True,
            Version("2.0.0"),
            id="yanked sdists",
        ),
        pytest.param(
            [
                ("2.0.0", "sdist", False),
                ("2.5.0", "sdist", False),
                ("1.0.0", "sdist", False),
            ],
            True,
            Version("2.5.0"),
            id="jumbled sdists",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.5b0", "sdist", False),
            ],
            True,
            Version("2.0.0"),
            id="pre_lease sdist",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", True),
                ("2.5b0", "sdist", False),
            ],
            True,
            Version("1.0.0"),
            id="pre_release and yanked sdists",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("invalid", "sdist", False),
            ],
            True,
            Version("1.0.0"),
            id="Invalid version does not fail",
        ),
    ],
)
def test_get_latest_version_sdists(packages_data, non_pre_release, expected):
    """
    Test examples are all sdists as piplexed only finds versions for sdists
    """
    packages = [
        create_autospec(DistributionPackage, version=v, package_type=t, is_yanked=y) for v, t, y in packages_data
    ]
    assert latest_pypi_version(packages, stable=non_pre_release) == expected


@pytest.mark.parametrize(
    "packages_data, non_pre_release, expected",
    [
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.5.0", "wheel", False),
            ],
            True,
            Version("2.0.0"),
            id="single wheel",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.0.0", "wheel", False),
            ],
            True,
            Version("2.0.0"),
            id="sdist and wheel",
        ),
        pytest.param(
            [
                ("2.0.0", "sdist", False),
                ("2.5.0", "wheel", False),
                ("1.0.0", "sdist", False),
            ],
            True,
            Version("2.0.0"),
            id="jumbled single wheel",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", False),
                ("2.5.0", "wheel", True),
            ],
            True,
            Version("2.0.0"),
            id="single yanked wheel",
        ),
        pytest.param(
            [
                ("1.0.0", "sdist", False),
                ("2.0.0", "sdist", True),
                ("2.5.0", "wheel", False),
            ],
            True,
            Version("1.0.0"),
            id="single wheel yanked sdist",
        ),
    ],
)
def test_get_latest_version_wheels(packages_data, non_pre_release, expected):
    """
    Piplexed only finds versions for sdists, this test, this test ensures wheels
    aren't included.
    """
    packages = [
        create_autospec(DistributionPackage, version=v, package_type=t, is_yanked=y) for v, t, y in packages_data
    ]
    assert latest_pypi_version(packages, stable=non_pre_release) == expected


@patch("piplexed.pypi_info.pypi_package_info")
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

    result = get_pypi_versions(client=mock_client, package=package, stable=True)
    assert [result] == [
        PackageInfo(name="testproj", version=Version("0.5.0"), python=None, latest_pypi_version=Version("2.5.0"))
    ]


# -----------------------------------------------------
# To test find_outdated_packages need to mock some data


@pytest.fixture
def mock_get_pipx_metadata():
    with patch("piplexed.pypi_info.get_pipx_metadata") as mock:
        mock.return_value = [
            PackageInfo(name="package1", version="1.0.0"),
            PackageInfo(name="package2", version="2.0.0"),
        ]
        yield mock


@pytest.fixture
def mock_get_pypi_versions():
    """
    In find_outdated_packages get_pypi_version is called for each package
    returned from get_pipx_metadata. Use side effects to get different results
    for each package.
    """
    with patch("piplexed.pypi_info.get_pypi_versions") as mock:

        def side_effect(client, pkg, stable):  # noqa: ARG001
            if pkg.name == "package1":
                return PackageInfo(
                    name="package1", version="1.0.0", latest_pypi_version="1.1.0" if stable else "1.2.0-beta"
                )
            else:
                return PackageInfo(name="package2", version="2.0.0", latest_pypi_version="2.0.0")

        mock.side_effect = side_effect
        yield mock


def test_find_outdated_packages(tmp_path, mock_get_pipx_metadata, mock_get_pypi_versions):
    result = find_outdated_packages(cache_dir=tmp_path / "cache")
    assert len(result) == 1
    assert result[0].name == "package1"
    assert result[0].version == "1.0.0"
    assert result[0].latest_pypi_version == "1.1.0"

    mock_get_pipx_metadata.assert_called_once()
    assert mock_get_pypi_versions.call_count == 2


def test_find_outdated_packages_unstable(tmp_path, mock_get_pipx_metadata, mock_get_pypi_versions):
    result = find_outdated_packages(cache_dir=tmp_path / "cache", stable=False)
    assert len(result) == 1
    assert result[0].name == "package1"
    assert result[0].version == "1.0.0"
    assert result[0].latest_pypi_version == "1.2.0-beta"

    mock_get_pipx_metadata.assert_called_once()
    assert mock_get_pypi_versions.call_count == 2


def test_find_outdated_packages_no_updates(tmp_path, mock_get_pipx_metadata, mock_get_pypi_versions):
    mock_get_pypi_versions.side_effect = lambda client, pkg, stable: (  # noqa: ARG005
        PackageInfo(name="package1", version="1.0.0", latest_pypi_version="1.0.0" if not stable else "1.0.0")
        if pkg.name == "package1"
        else PackageInfo(name="package2", version="2.0.0", latest_pypi_version="2.0.0")
    )

    result = find_outdated_packages(cache_dir=tmp_path / "cache")
    assert not result
    mock_get_pipx_metadata.assert_called_once()
    assert mock_get_pypi_versions.call_count == 2


def test_find_outdated_packages_unstable_no_updates(tmp_path, mock_get_pipx_metadata, mock_get_pypi_versions):
    mock_get_pypi_versions.side_effect = lambda client, pkg, stable: (  # noqa: ARG005
        PackageInfo(name="package1", version="1.0.0", latest_pypi_version="1.0.0" if not stable else "1.0.0")
        if pkg.name == "package1"
        else PackageInfo(name="package2", version="2.0.0", latest_pypi_version="2.0.0")
    )

    result = find_outdated_packages(cache_dir=tmp_path / "cache", stable=False)
    assert not result
    mock_get_pipx_metadata.assert_called_once()
    assert mock_get_pypi_versions.call_count == 2
