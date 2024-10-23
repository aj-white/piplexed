from __future__ import annotations

import typer

import piplexed
from piplexed._print_table import print_list_table
from piplexed._print_table import print_outdated_table
from piplexed._print_tree import print_list_outdated
from piplexed._print_tree import print_list_tree
from piplexed.pipx_venvs import ToolType

app = typer.Typer()


@app.command()
def version() -> None:
    print(piplexed.__version__)


@app.command()
def list(
    outdated: bool = typer.Option(False, "--outdated", "-O", help="Find outdated packages installed with pipx"),
    is_prelease: bool = typer.Option(
        False,
        "--pre",
        "-P",
        help="Include pre and dev releases in latest pypi version search",
    ),
    tree: bool = typer.Option(False, "--tree", "-T", help="print output as a tree (default is table)"),
    tool: ToolType = typer.Option(
        "pipx", "--tool", help="choose tool packages were installed with, 'pipx', 'uv', 'both"
    ),
) -> None:
    if outdated and is_prelease and tree:
        print_list_outdated(piplexed.find_outdated_packages(stable=False, tool=tool))
    elif outdated and is_prelease:
        print_outdated_table(piplexed.find_outdated_packages(stable=False, tool=tool))
    elif outdated and tree and not is_prelease:
        print_list_outdated(piplexed.find_outdated_packages(stable=True, tool=tool))
    elif outdated and not is_prelease:
        print_outdated_table(piplexed.find_outdated_packages(stable=True, tool=tool))
    elif tree:
        print_list_tree(piplexed.get_pipx_metadata())
    else:
        print_list_table(piplexed.get_pipx_metadata())


if __name__ == "__main__":
    raise SystemExit(app)
