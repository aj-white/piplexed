from unittest.mock import patch

from typer.testing import CliRunner

from piplexed.cli import app
from piplexed.version import VERSION

runner = CliRunner()


def test_cli_list():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == VERSION


def mock_installed_output(tree, tool):
    print(f"tree:{tree} tool:{tool.value}")


def mock_outdated_output(is_prerelease, tree, tool):
    print(f"is_prerelease:{is_prerelease} tree:{tree} tool:{tool.value}")


@patch("piplexed.cli.print_installed_tools", side_effect=mock_installed_output)
def test_list_cmd_defaults(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "tree:False tool:pipx" in result.stdout.strip()


@patch("piplexed.cli.print_installed_tools", side_effect=mock_installed_output)
def test_list_cmd_uv_default(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--tool", "uv"])
    assert result.exit_code == 0
    assert "tree:False tool:uv" in result.stdout.strip()


@patch("piplexed.cli.print_installed_tools", side_effect=mock_installed_output)
def test_list_cmd_pipx_tree(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--tree"])
    assert result.exit_code == 0
    assert "tree:True tool:pipx" in result.stdout.strip()


@patch("piplexed.cli.print_installed_tools", side_effect=mock_installed_output)
def test_list_cmd_uv_tree(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--tree", "--tool", "uv"])
    assert result.exit_code == 0
    assert "tree:True tool:uv" in result.stdout.strip()


def test_invalid_tool_option():
    result = runner.invoke(app, ["list", "--tool", "jeff"])
    assert result.exit_code != 0


@patch("piplexed.cli.print_installed_tools", side_effect=mock_installed_output)
def test_use_of_prerelease_has_no_effect_on_installed(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--pre"])
    assert result.exit_code == 0
    assert "tree:False tool:pipx" in result.stdout.strip()


@patch("piplexed.cli.print_outdated_tools", side_effect=mock_outdated_output)
def test_list_cmd_outdated_defaults(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--outdated"])
    assert result.exit_code == 0
    assert "is_prerelease:False tree:False tool:pipx" in result.stdout.strip()


@patch("piplexed.cli.print_outdated_tools", side_effect=mock_outdated_output)
def test_list_cmd_outdated_pipx_tree(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--outdated", "--tree"])
    assert result.exit_code == 0
    assert "is_prerelease:False tree:True tool:pipx" in result.stdout.strip()


@patch("piplexed.cli.print_outdated_tools", side_effect=mock_outdated_output)
def test_list_cmd_outdated_pipx_prerelease(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--outdated", "--pre"])
    assert result.exit_code == 0
    assert "is_prerelease:True tree:False tool:pipx" in result.stdout.strip()


@patch("piplexed.cli.print_outdated_tools", side_effect=mock_outdated_output)
def test_list_cmd_outdated_pipx_prerelease_tree(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--outdated", "--pre", "--tree"])
    assert result.exit_code == 0
    assert "is_prerelease:True tree:True tool:pipx" in result.stdout.strip()


@patch("piplexed.cli.print_outdated_tools", side_effect=mock_outdated_output)
def test_list_cmd_outdated_uv_defaults(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--outdated", "--tool", "uv"])
    assert result.exit_code == 0
    assert "is_prerelease:False tree:False tool:uv" in result.stdout.strip()


@patch("piplexed.cli.print_outdated_tools", side_effect=mock_outdated_output)
def test_list_cmd_outdated_uv_tree(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--outdated", "--tree", "--tool", "uv"])
    assert result.exit_code == 0
    assert "is_prerelease:False tree:True tool:uv" in result.stdout.strip()


@patch("piplexed.cli.print_outdated_tools", side_effect=mock_outdated_output)
def test_list_cmd_outdated_uv_prerelease(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--outdated", "--pre", "--tool", "uv"])
    assert result.exit_code == 0
    assert "is_prerelease:True tree:False tool:uv" in result.stdout.strip()


@patch("piplexed.cli.print_outdated_tools", side_effect=mock_outdated_output)
def test_list_cmd_outdated_uv_prerelease_tree(installed_package):
    installed_package.return_value = None
    result = runner.invoke(app, ["list", "--outdated", "--pre", "--tree", "--tool", "uv"])
    assert result.exit_code == 0
    assert "is_prerelease:True tree:True tool:uv" in result.stdout.strip()
