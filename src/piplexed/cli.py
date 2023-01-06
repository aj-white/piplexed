import typer
import piplexed
from piplexed._print_tree import print_list_tree

app = typer.Typer()


@app.command()
def version() -> None:
    print(piplexed.__version__)


@app.command()
def list(
    outdated: bool = typer.Option(False, "--outdated", "-O", help="Find outdated packages installed with pipx"),
    is_prelease: bool = typer.Option(
        False, "--pre", "-P", help="Include pre and dev releases in latest pypi version search"
    ),
):
    if outdated and is_prelease:
        print(piplexed.find_outdated_packages(stable=False))
    elif outdated and not is_prelease:
        print(piplexed.find_outdated_packages())
    else:
        print_list_tree(piplexed.get_pipx_metadata())


if __name__ == "__main__":
    raise SystemExit(app)
