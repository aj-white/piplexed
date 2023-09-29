from __future__ import annotations

import typer

import piplexed
from piplexed._print_table import print_list_table
from piplexed._print_table import print_outdated_table
from piplexed._print_tree import print_list_outdated
from piplexed._print_tree import print_list_tree

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
    table: bool = typer.Option(False, "--table", "-T", help="print output as a table"),
) -> None:
    if outdated and is_prelease and table:
        print_outdated_table(piplexed.find_outdated_packages(stable=False))
    elif outdated and is_prelease:
        print_list_outdated(piplexed.find_outdated_packages(stable=False))
    elif outdated and table and not is_prelease:
        print_outdated_table(piplexed.find_outdated_packages(stable=True))
    elif outdated and not is_prelease:
        print_list_outdated(piplexed.find_outdated_packages(stable=True))
    elif table:
        print_list_table(piplexed.get_pipx_metadata())
    else:
        print_list_tree(piplexed.get_pipx_metadata())


if __name__ == "__main__":
    raise SystemExit(app)
