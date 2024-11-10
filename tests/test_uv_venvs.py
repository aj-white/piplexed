from pathlib import Path
from unittest.mock import patch

import pytest
from packaging.version import Version

from piplexed.venvs import PackageInfo
from piplexed.venvs.uv_venvs import find_uv_tool_dir
from piplexed.venvs.uv_venvs import get_python_path
from piplexed.venvs.uv_venvs import installed_uv_tools
from piplexed.venvs.uv_venvs import uv_tool_version


@patch("piplexed.venvs.uv_venvs.shutil.which")
def test_find_uv_tool_dir(mock_uv_path, fp):
    mock_uv_path.return_value = "mock/path/uv"

    fp.register(["mock/path/uv", "tool", "dir"], stdout="uv/tool/dir")

    result = find_uv_tool_dir()
    assert result == "uv/tool/dir"


@patch("piplexed.venvs.uv_venvs.shutil.which")
def test_no_uv(mock_uv_path):
    mock_uv_path.return_value = "mock/path/uv"

    with pytest.raises(FileNotFoundError):
        find_uv_tool_dir()


@patch("piplexed.venvs.uv_venvs.shutil.which")
def test_uv_tool_dir_failed_returncode(mock_uv_path, fp):
    def callback_function(process):
        process.returncode = 1

    mock_uv_path.return_value = "mock/path/uv"

    fp.register(["mock/path/uv", "tool", "dir"], stdout="uv/tool/dir", callback=callback_function)

    with pytest.raises(FileNotFoundError):
        find_uv_tool_dir()


def test_uv_tool_version_windows(tmp_path, fp):
    mock_tool_dir = tmp_path / "package1"
    mock_tool_python = mock_tool_dir / "Scripts" / "python.exe"

    script = "from importlib.metadata import version; print(version('package1'))"
    fp.register([mock_tool_python, "-c", script], stdout="1.0.1")

    result = uv_tool_version(mock_tool_dir, "Windows")

    assert result == "1.0.1"


def test_uv_tool_version_linux(tmp_path, fp):
    mock_tool_dir = tmp_path / "package1"
    mock_tool_python = mock_tool_dir / "bin" / "python"

    script = "from importlib.metadata import version; print(version('package1'))"
    fp.register([mock_tool_python, "-c", script], stdout="1.0.1")

    result = uv_tool_version(mock_tool_dir, "Linux")

    assert result == "1.0.1"


@pytest.mark.parametrize(
    "op_system, expected",
    [
        pytest.param("Windows", Path("Scripts") / "python.exe", id="windows"),
        pytest.param("Linux", Path("bin") / "python", id="linux"),
        pytest.param("Darwin", Path("bin") / "python", id="macOS"),
    ],
)
def test_get_python_path(tmp_path, op_system, expected):
    mock_venv = tmp_path / "package1"
    result = get_python_path(mock_venv, op_system)
    assert result == Path.joinpath(mock_venv, expected)


@patch("piplexed.venvs.uv_venvs.get_python_path")
def test_installed_uv_tools_windows(mock_py_path, tmp_path, fp):
    mock_tools_venv = tmp_path / "venvs"
    mock_tools_venv.mkdir()

    test_ignore_path = mock_tools_venv / ".tester"
    test_ignore_path.mkdir()

    package_1 = mock_tools_venv / "package1"
    package_1.mkdir()

    mock_py_path.return_value = package_1 / "Scripts" / "python.exe"

    package_version_cmd = f"from importlib.metadata import version; print(version('{package_1.name}'))"
    python_version_cmd = "import sys; print(sys.version.split()[0])"
    fp.register([package_1 / "Scripts" / "python.exe", "-c", package_version_cmd], stdout="1.0.1")
    fp.register([package_1 / "Scripts" / "python.exe", "-c", python_version_cmd], stdout="3.12.7")

    result = installed_uv_tools(mock_tools_venv, "Windows")
    assert result == [PackageInfo(name="package1", version=Version("1.0.1"), python="3.12.7", tool="uv")]


@patch("piplexed.venvs.uv_venvs.get_python_path")
def test_installed_uv_tools_linux(mock_py_path, tmp_path, fp):
    mock_tools_venv = tmp_path / "venvs"
    mock_tools_venv.mkdir()

    test_ignore_path = mock_tools_venv / ".tester"
    test_ignore_path.mkdir()

    package_1 = mock_tools_venv / "package1"
    package_1.mkdir()

    mock_py_path.return_value = package_1 / "bin" / "python"

    package_version_cmd = f"from importlib.metadata import version; print(version('{package_1.name}'))"
    python_version_cmd = "import sys; print(sys.version.split()[0])"
    fp.register([package_1 / "bin" / "python", "-c", package_version_cmd], stdout="1.0.1")
    fp.register([package_1 / "bin" / "python", "-c", python_version_cmd], stdout="3.12.7")

    result = installed_uv_tools(mock_tools_venv, "Linux")
    assert result == [PackageInfo(name="package1", version=Version("1.0.1"), python="3.12.7", tool="uv")]
