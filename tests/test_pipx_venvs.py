from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
from packaging.version import Version

from piplexed.pipx_venvs import PackageInfo
from piplexed.pipx_venvs import get_local_venv
from piplexed.pipx_venvs import get_pipx_metadata
from piplexed.pipx_venvs import pipx_home_paths_for_os

PIPX_METADATA_VERSIONS = [None, "0.1", "0.2", "0.3", "0.4", "0.5"]

# Metadata changes for 0.1 -> 0.3 and 0.4 -> 0.5 were at package level
MOCK_BASE_PIPX_METADATA: dict[str, Any] = {
    "main_package": None,
    "python_version": None,
    "venv_args": [],
    "injected_packages": {},
    "pipx_metadata_version": "0.1",
}

MOCK_PIPX_METADATA_0_4: dict[str, Any] = dict(MOCK_BASE_PIPX_METADATA, **{"source_interpreter": None})

MOCK_PACKAGE_DATA_0_1: dict[str, Any] = {
    "package": None,
    "package_or_url": None,
    "pip_args": [],
    "include_dependencies": False,
    "include_apps": True,
    "apps": [],
    "app_paths": [],
    "apps_of_dependencies": [],
    "app_paths_of_dependencies": {},
    "package_version": "",
}
# would like to use | operator e.g. # MOCK_PACKAGE_DATA_0_1 | {"suffix": ""} but not supported in python 3.8
MOCK_PACKAGE_DATA_0_2 = dict(MOCK_PACKAGE_DATA_0_1, **{"suffix": ""})

MOCK_PACKAGE_DATA_0_3_and_0_4 = dict(
    MOCK_PACKAGE_DATA_0_2,
    **{
        "man_pages": [],
        "man_paths": [],
        "man_pages_of_dependencies": [],
        "man_paths_of_dependencies": {},
    },
)

MOCK_PACKAGE_DATA_0_5 = dict(MOCK_PACKAGE_DATA_0_3_and_0_4, **{"pinned": False})


def mock_metadata(metadata_version: str, pypi_package: bool = True) -> dict[str, Any]:  # noqa: FBT001, FBT002
    if metadata_version in ["0.1", "0.2", "0.3"]:
        metadata_template = MOCK_BASE_PIPX_METADATA
    elif metadata_version in ["0.4", "0.5"]:
        metadata_template = MOCK_PIPX_METADATA_0_4
    else:
        err_msg = f"Internal Test Error: Unknown metadata_version={metadata_version}"
        raise Exception(err_msg)

    if metadata_version == "0.1":
        package_template = MOCK_PACKAGE_DATA_0_1
    elif metadata_version == "0.2":
        package_template = MOCK_PACKAGE_DATA_0_2
    elif metadata_version in ["0.3", "0.4"]:
        package_template = MOCK_PACKAGE_DATA_0_3_and_0_4
    elif metadata_version == "0.5":
        package_template = MOCK_PACKAGE_DATA_0_5
    else:
        err_msg = f"Internal Test Error: Unknown metadata_version={metadata_version}"
        raise Exception(err_msg)

    if pypi_package:
        package_template["package"] = "Testy_McTestFace"
        package_template["package_or_url"] = "Testy_McTestFace"
    else:
        package_template["package"] = "Local_Package"
        package_template["package_or_url"] = "path/to/local/wheel"

    package_template["package_version"] = "23.1.0"
    metadata_template["pipx_metadata_version"] = metadata_version
    metadata_template["python_version"] = "Python 3.11.2"
    metadata_template["main_package"] = package_template

    return metadata_template


@pytest.fixture
def venv_dir_test_setup(tmp_path):
    env_dir = tmp_path / "venvs"
    env_dir.mkdir()
    pypi_package = env_dir / "pypi_package"
    pypi_package.mkdir()
    local_package = env_dir / "local_package"
    local_package.mkdir()

    return env_dir


@pytest.mark.parametrize("pipx_metadata_version", ("0.1", "0.2", "0.3", "0.4", "0.5"))
def test_pipx_metadata(venv_dir_test_setup, pipx_metadata_version):
    pypi_json = venv_dir_test_setup / "pypi_package" / "pipx_metadata.json"
    local_json = venv_dir_test_setup / "local_package" / "pipx_metadata.json"

    expected = [PackageInfo(name="testy-mctestface", version=Version("23.1.0"), python="3.11.2")]

    with open(pypi_json, "w") as f:
        pipx_metadata = mock_metadata(metadata_version=pipx_metadata_version)
        json.dump(pipx_metadata, f)

    with open(local_json, "w") as f:
        pipx_metadata = mock_metadata(metadata_version=pipx_metadata_version, pypi_package=False)
        json.dump(pipx_metadata, f)

    assert get_pipx_metadata(venv_dir_test_setup) == expected


def test_multiple_json_files_in_venv(venv_dir_test_setup):
    pypi_json = venv_dir_test_setup / "pypi_package" / "pipx_metadata.json"
    extra_json = venv_dir_test_setup / "pypi_package" / "schema.json"

    expected = [PackageInfo(name="testy-mctestface", version=Version("23.1.0"), python="3.11.2")]

    with open(pypi_json, "w") as f:
        pipx_metadata = mock_metadata(metadata_version="0.5")
        json.dump(pipx_metadata, f)

    with open(extra_json, "w") as f:
        extra_data = {"test": "test extra data"}
        json.dump(extra_data, f)

    assert get_pipx_metadata(venv_dir_test_setup) == expected


def test_venv_dir_is_none():
    with pytest.raises(FileNotFoundError) as execinfo:
        get_pipx_metadata(venv_dir=None)

    assert str(execinfo.value) == "Unable to find pipx venv installation location"


def test_venv_dir_not_exists(tmp_path):
    non_existent_path = tmp_path / "joker"
    with pytest.raises(FileNotFoundError) as execinfo:
        get_pipx_metadata(venv_dir=non_existent_path)

    assert str(execinfo.value) == "Unable to find pipx venv installation location"


@pytest.fixture
def mock_user_data_path():
    with patch("piplexed.pipx_venvs.user_data_path") as mock_user_data:
        mock_user_data.return_value = "mock/user/data/pipx"
        yield mock_user_data


def test_pipx_home_paths_for_os_linux(mock_user_data_path):  # noqa: ARG001
    default, fallback = pipx_home_paths_for_os("Linux")
    assert str(default) == os.path.join("mock", "user", "data", "pipx")
    assert [str(p) for p in fallback] == [
        os.path.join(str(Path.home()), ".local", "pipx"),
    ]


def test_pipx_home_paths_for_os_windows(mock_user_data_path):  # noqa: ARG001
    default, fallback = pipx_home_paths_for_os("Windows")
    assert str(default) == os.path.join(str(Path.home()), "pipx")
    assert [str(p) for p in fallback] == [
        os.path.join(str(Path.home()), ".local", "pipx"),
        os.path.join("mock", "user", "data", "pipx"),
    ]


def test_pipx_home_paths_for_os_other(mock_user_data_path):  # noqa: ARG001
    default, fallback = pipx_home_paths_for_os("Darwin")
    assert str(default) == os.path.join(str(Path.home()), ".local", "pipx")
    assert [str(p) for p in fallback] == [os.path.join("mock", "user", "data", "pipx")]


@pytest.fixture
def mock_pipx_homes(monkeypatch, tmp_path):
    default_home = tmp_path / "default"
    fallback_homes = [tmp_path / "fallback1", tmp_path / "fallback2"]

    monkeypatch.setattr("piplexed.pipx_venvs.DEFAULT_PIPX_HOME", default_home)
    monkeypatch.setattr("piplexed.pipx_venvs.FALLBACK_PIPX_HOMES", fallback_homes)

    return (default_home, fallback_homes)


def test_default_pipx_home_exists(mock_pipx_homes):
    default_home, _ = mock_pipx_homes
    default_home.mkdir()

    result = get_local_venv()
    assert result == default_home / "venvs"


def test_default_pipx_home_not_exists_fallback1_exists(mock_pipx_homes):
    _, fallbacks = mock_pipx_homes
    fallback_1 = fallbacks[0]
    fallback_1.mkdir()
    result = get_local_venv()
    assert result == fallback_1 / "venvs"


def test_default_pipx_home_not_exists_fallback2_exists(mock_pipx_homes):
    _, fallbacks = mock_pipx_homes
    fallback_2 = fallbacks[1]
    fallback_2.mkdir()
    result = get_local_venv()
    assert result == fallback_2 / "venvs"


def test_default_pipx_home_not_exists_fallback1_and_fallback2_exists(mock_pipx_homes):
    _, fallbacks = mock_pipx_homes
    fallback_1 = fallbacks[0]
    fallback_2 = fallbacks[1]
    fallback_1.mkdir()
    fallback_2.mkdir()
    result = get_local_venv()
    assert result == fallback_1 / "venvs"


def test_default_pipx_home_exists_and_fallback_exists(mock_pipx_homes):
    default, fallbacks = mock_pipx_homes
    fallback_1 = fallbacks[0]
    fallback_2 = fallbacks[1]
    default.mkdir()
    fallback_1.mkdir()
    fallback_2.mkdir()
    result = get_local_venv()
    assert result == default / "venvs"


def test_default_pipx_home_not_exists_and_fallback_not_exists(mock_pipx_homes):
    default, fallbacks = mock_pipx_homes
    result = get_local_venv()
    assert result is None
