from __future__ import annotations

import typer

import piplexed
from piplexed.app import print_installed_tools
from piplexed.app import print_outdated_tools
from piplexed.venvs import ToolType

app = typer.Typer()


@app.command()
def version() -> None:
    print(piplexed.__version__)


@app.command()
def list(
    outdated: bool = typer.Option(False, "--outdated", "-O", help="Find outdated packages installed with pipx"),
    is_prerelease: bool = typer.Option(
        False,
        "--pre",
        "-P",
        help="Include pre and dev releases in latest pypi version search",
    ),
    tree: bool = typer.Option(False, "--tree", "-T", help="print output as a tree (default is table)"),
    tool: ToolType = typer.Option(
        "pipx", "--tool", help="choose tool packages were installed with, 'pipx', 'uv', 'all"
    ),
) -> None:
    if outdated:
        print_outdated_tools(is_prerelease=is_prerelease, tree=tree, tool=tool)
    else:
        print_installed_tools(tree=tree, tool=tool)


if __name__ == "__main__":
    raise SystemExit(app)
