from __future__ import annotations

import typer

import piplexed
from piplexed._print_table import print_list_table
from piplexed._print_table import print_outdated_table
from piplexed._print_tree import print_list_outdated
from piplexed._print_tree import print_list_tree
from piplexed.utils import future_deprecation_warning

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
    future_deprecation_warning(
        reason="The table view will become the default option, "
        "due to it being more clear and concise than the tree view. "
        "There will be no need to pass '--table'",
        replacement="To get the tree view in future versions, '--tree'/'-T' will need to be passed as options",
        deprecation_version="v0.4.0",
    )
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
