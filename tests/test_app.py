from unittest.mock import patch

import pytest
from packaging.version import Version

from piplexed import app
from piplexed.venvs import PackageInfo
from piplexed.venvs import ToolType


@pytest.fixture()
def pipx_package():
    return PackageInfo(
        name="package1", version=Version("1.0.1"), python="3.12.7", latest_pypi_version=Version("1.5.0"), tool="pipx"
    )


@pytest.fixture()
def uv_package():
    return PackageInfo(
        name="package2", version=Version("2.0.5"), python="3.12.7", latest_pypi_version=Version("2.0.6"), tool="uv"
    )


@patch("piplexed.app.installed_pipx_tools")
def test_find_installed_tools_pipx(pipx_tools, pipx_package):
    expected = [pipx_package]
    pipx_tools.return_value = expected

    assert app.find_installed_tools(ToolType.PIPX) == expected


@patch("piplexed.app.installed_uv_tools")
def test_find_installed_tools_uv(uv_tools, uv_package):
    expected = [uv_package]
    uv_tools.return_value = expected

    assert app.find_installed_tools(ToolType.UV) == expected


@patch("piplexed.app.installed_uv_tools")
@patch("piplexed.app.installed_pipx_tools")
def test_find_installed_tools_all(pipx_tools, uv_tools, pipx_package, uv_package):
    expected = [
        pipx_package,
        uv_package,
    ]
    pipx_tools.return_value = [expected[0]]
    uv_tools.return_value = [expected[1]]

    assert app.find_installed_tools(ToolType.ALL) == expected


@patch("piplexed.app.installed_pipx_tools")
def test_find_installed_tools_pipx_none(pipx_tools):
    #  installed tools will return empty list if can't find any tools
    pipx_tools.return_value = []

    with pytest.raises(FileNotFoundError):
        app.find_installed_tools(ToolType.PIPX)


@patch("piplexed.app.installed_uv_tools")
def test_find_installed_tools_uv_none(uv_tools):
    uv_tools.return_value = []

    with pytest.raises(FileNotFoundError):
        app.find_installed_tools(ToolType.UV)


@patch("piplexed.app.installed_uv_tools")
@patch("piplexed.app.installed_pipx_tools")
def test_find_installed_tools_all_but_uv_none(pipx_tools, uv_tools, pipx_package):
    expected = [
        pipx_package,
    ]
    pipx_tools.return_value = expected
    uv_tools.return_value = []

    assert app.find_installed_tools(ToolType.ALL) == expected


@patch("piplexed.app.installed_uv_tools")
@patch("piplexed.app.installed_pipx_tools")
def test_find_installed_tools_all_but_pipx_none(pipx_tools, uv_tools, uv_package):
    expected = [
        uv_package,
    ]
    pipx_tools.return_value = []
    uv_tools.return_value = expected

    assert app.find_installed_tools(ToolType.ALL) == expected


@patch("piplexed.app.installed_uv_tools")
@patch("piplexed.app.installed_pipx_tools")
def test_find_installed_tools_all_but_pipx_and_uv_none(pipx_tools, uv_tools):
    pipx_tools.return_value = []
    uv_tools.return_value = []

    with pytest.raises(FileNotFoundError):
        app.find_installed_tools(ToolType.ALL)


@patch("piplexed.app.find_installed_tools")
def test_print_installed_tools_pipx_table(mock_tools, pipx_package, capsys: pytest.CaptureFixture[str]):
    mock_tools.return_value = [pipx_package]
    app.print_installed_tools(tree=False, tool=ToolType.PIPX)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    headers = (
        "Package Name",
        "Installed Version",
        "Python Version",
    )
    assert output[0].startswith("PIPX Packages")
    assert all(header in output[2] for header in headers)
    assert output[4] == "│     package1 │             1.0.1 │         3.12.7 │"


@patch("piplexed.app.find_installed_tools")
def test_print_installed_tools_uv_table(mock_tools, uv_package, capsys: pytest.CaptureFixture[str]):
    mock_tools.return_value = [uv_package]
    app.print_installed_tools(tree=False, tool=ToolType.UV)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    headers = (
        "Package Name",
        "Installed Version",
        "Python Version",
    )
    assert output[0].startswith("UV Packages")
    assert all(header in output[2] for header in headers)
    assert output[4] == "│     package2 │             2.0.5 │         3.12.7 │"


@patch("piplexed.app.find_installed_tools")
def test_print_installed_tools_all_table(mock_tools, pipx_package, uv_package, capsys: pytest.CaptureFixture[str]):
    mock_tools.return_value = [pipx_package, uv_package]
    app.print_installed_tools(tree=False, tool=ToolType.ALL)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    headers = (
        "Package Name",
        "Installed Version",
        "Python Version",
    )
    assert output[0].startswith("PIPX Packages")
    assert all(header in output[2] for header in headers)
    assert output[4] == "│     package1 │             1.0.1 │         3.12.7 │"
    assert output[6].startswith("UV Packages")
    assert all(header in output[8] for header in headers)
    assert output[10] == "│     package2 │             2.0.5 │         3.12.7 │"


@patch("piplexed.app.find_installed_tools")
def test_print_installed_tools_pipx_tree(mock_tools, pipx_package, capsys: pytest.CaptureFixture[str]):
    mock_tools.return_value = [pipx_package]
    app.print_installed_tools(tree=True, tool=ToolType.PIPX)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    assert output[0].startswith("PIPX Packages")
    assert output[1] == "└── Package1"
    assert output[2] == "├── version - 1.0.1"
    assert output[3] == "└── python - 3.12.7"


@patch("piplexed.app.find_installed_tools")
def test_print_installed_tools_uv_tree(mock_tools, uv_package, capsys: pytest.CaptureFixture[str]):
    mock_tools.return_value = [uv_package]
    app.print_installed_tools(tree=True, tool=ToolType.UV)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    assert output[0].startswith("UV Packages")
    assert output[1] == "└── Package2"
    assert output[2] == "├── version - 2.0.5"
    assert output[3] == "└── python - 3.12.7"


@patch("piplexed.app.find_installed_tools")
def test_print_installed_tools_all_tree(mock_tools, pipx_package, uv_package, capsys: pytest.CaptureFixture[str]):
    mock_tools.return_value = [pipx_package, uv_package]
    app.print_installed_tools(tree=True, tool=ToolType.ALL)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    assert output[0].startswith("PIPX Packages")
    assert output[1] == "└── Package1"
    assert output[2] == "├── version - 1.0.1"
    assert output[3] == "└── python - 3.12.7"
    assert output[4].startswith("UV Packages")
    assert output[5] == "└── Package2"
    assert output[6] == "├── version - 2.0.5"
    assert output[7] == "└── python - 3.12.7"


@patch("piplexed.app.find_most_recent_version_on_pypi")
@patch("piplexed.app.find_installed_tools")
def test_print_outdated_tools_pipx_table(mock_tools, mock_outdated, pipx_package, capsys):
    mock_tools.return_value = [pipx_package]
    mock_outdated.return_value = [pipx_package]
    app.print_outdated_tools(is_prerelease=False, tree=False, tool=ToolType.PIPX)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    headers = (
        "Package Name",
        "Installed Version",
        "PyPI Version",
    )
    assert output[0].startswith("PIPX Outdated Packages")
    assert all(header in output[2] for header in headers)
    assert output[4] == "│     package1 │             1.0.1 │        1.5.0 │"


@patch("piplexed.app.find_most_recent_version_on_pypi")
@patch("piplexed.app.find_installed_tools")
def test_print_outdated_tools_uv_table(mock_tools, mock_outdated, uv_package, capsys):
    mock_tools.return_value = [uv_package]
    mock_outdated.return_value = [uv_package]
    app.print_outdated_tools(is_prerelease=False, tree=False, tool=ToolType.UV)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    headers = (
        "Package Name",
        "Installed Version",
        "PyPI Version",
    )
    assert output[0].startswith("UV Outdated Packages")
    assert all(header in output[2] for header in headers)
    assert output[4] == "│     package2 │             2.0.5 │        2.0.6 │"


@patch("piplexed.app.find_most_recent_version_on_pypi")
@patch("piplexed.app.find_installed_tools")
def test_print_outdated_tools_all_table(mock_tools, mock_outdated, pipx_package, uv_package, capsys):
    mock_tools.return_value = [pipx_package, uv_package]
    mock_outdated.return_value = [pipx_package, uv_package]
    app.print_outdated_tools(is_prerelease=False, tree=False, tool=ToolType.ALL)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    headers = (
        "Package Name",
        "Installed Version",
        "PyPI Version",
    )
    assert output[0].startswith("PIPX Outdated Packages")
    assert all(header in output[2] for header in headers)
    assert output[4] == "│     package1 │             1.0.1 │        1.5.0 │"
    assert output[6].startswith("UV Outdated Packages")
    assert all(header in output[8] for header in headers)
    assert output[10] == "│     package2 │             2.0.5 │        2.0.6 │"


@patch("piplexed.app.find_most_recent_version_on_pypi")
@patch("piplexed.app.find_installed_tools")
def test_print_outdateded_packages_pipx_tree(
    mock_tools, mock_outdated, pipx_package, capsys: pytest.CaptureFixture[str]
):
    mock_tools.return_value = [pipx_package]
    mock_outdated.return_value = [pipx_package]
    app.print_outdated_tools(is_prerelease=False, tree=True, tool=ToolType.PIPX)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    assert output[0].startswith("PIPX Outdated Packages")
    assert output[1] == "└── Package1"
    assert output[2] == "├── installed version - 1.0.1"
    assert output[3] == "└── PyPI version - 1.5.0"


@patch("piplexed.app.find_most_recent_version_on_pypi")
@patch("piplexed.app.find_installed_tools")
def test_print_outdateded_packages_uv_tree(mock_tools, mock_outdated, uv_package, capsys: pytest.CaptureFixture[str]):
    mock_tools.return_value = [uv_package]
    mock_outdated.return_value = [uv_package]
    app.print_outdated_tools(is_prerelease=False, tree=True, tool=ToolType.UV)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    assert output[0].startswith("UV Outdated Packages")
    assert output[1] == "└── Package2"
    assert output[2] == "├── installed version - 2.0.5"
    assert output[3] == "└── PyPI version - 2.0.6"


@patch("piplexed.app.find_most_recent_version_on_pypi")
@patch("piplexed.app.find_installed_tools")
def test_print_outdateded_packages_all_tree(
    mock_tools, mock_outdated, pipx_package, uv_package, capsys: pytest.CaptureFixture[str]
):
    mock_tools.return_value = [pipx_package, uv_package]
    mock_outdated.return_value = [pipx_package, uv_package]
    app.print_outdated_tools(is_prerelease=False, tree=True, tool=ToolType.ALL)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    assert output[0].startswith("PIPX Outdated Packages")
    assert output[1] == "└── Package1"
    assert output[2] == "├── installed version - 1.0.1"
    assert output[3] == "└── PyPI version - 1.5.0"
    assert output[4].startswith("UV Outdated Packages")
    assert output[5] == "└── Package2"
    assert output[6] == "├── installed version - 2.0.5"
    assert output[7] == "└── PyPI version - 2.0.6"


@patch("piplexed.app.find_most_recent_version_on_pypi")
@patch("piplexed.app.find_installed_tools")
def test_print_outdateded_packages_pipx_no_updates(
    mock_tools, mock_outdated, pipx_package, capsys: pytest.CaptureFixture[str]
):
    mock_tools.return_value = [pipx_package]
    mock_outdated.return_value = []
    app.print_outdated_tools(is_prerelease=False, tree=True, tool=ToolType.PIPX)

    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == "✨ Installed packages are all up to date ✨"


@patch("piplexed.app.find_most_recent_version_on_pypi")
@patch("piplexed.app.find_installed_tools")
def test_print_outdateded_packages_uv_no_updates(
    mock_tools, mock_outdated, uv_package, capsys: pytest.CaptureFixture[str]
):
    mock_tools.return_value = [uv_package]
    mock_outdated.return_value = []
    app.print_outdated_tools(is_prerelease=False, tree=True, tool=ToolType.UV)

    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == "✨ Installed packages are all up to date ✨"


@patch("piplexed.app.find_most_recent_version_on_pypi")
@patch("piplexed.app.find_installed_tools")
def test_print_outdateded_packages_all_no_updates(
    mock_tools, mock_outdated, pipx_package, uv_package, capsys: pytest.CaptureFixture[str]
):
    mock_tools.return_value = [pipx_package, uv_package]
    mock_outdated.return_value = []
    app.print_outdated_tools(is_prerelease=False, tree=True, tool=ToolType.ALL)

    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == "✨ Installed packages are all up to date ✨"
