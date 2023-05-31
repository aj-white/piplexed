from unittest.mock import create_autospec
from unittest.mock import patch

import pytest
from packaging.version import Version
from pypi_simple import DistributionPackage
from pypi_simple import ProjectPage

from piplexed.pipx_venvs import PackageInfo
from piplexed.pypi_info import get_latest_version
from piplexed.pypi_info import get_pypi_versions


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
    assert get_latest_version(packages, stable=non_pre_release) == expected


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
    ],
)
def test_get_latest_version_sdists(packages_data, non_pre_release, expected):
    packages = [
        create_autospec(DistributionPackage, version=v, package_type=t, is_yanked=y) for v, t, y in packages_data
    ]
    assert get_latest_version(packages, stable=non_pre_release) == expected


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
    packages = [
        create_autospec(DistributionPackage, version=v, package_type=t, is_yanked=y) for v, t, y in packages_data
    ]
    assert get_latest_version(packages, stable=non_pre_release) == expected


@patch("pypi_simple.PyPISimple.get_project_page")
def test_get_pypi_versions(mock_page):
    packages_data = [
        ("1.0.0", "sdist", False),
        ("2.0.0", "sdist", False),
        ("2.5.0", "sdist", False),
    ]
    packages = [
        create_autospec(DistributionPackage, version=v, package_type=t, is_yanked=y) for v, t, y in packages_data
    ]

    page = create_autospec(ProjectPage, project="testproj", packages=packages)
    mock_page.return_value = page

    result = get_pypi_versions(session=None, package_name="testproj", stable=True)
    assert list(result) == [PackageInfo(name="testproj", version=Version("2.5.0"), python=None)]
