from __future__ import annotations

import warnings
from os import getenv

from rich.console import Console
from rich.panel import Panel

TERMINAL_WIDTH = getenv("TERMINAL_WIDTH")


def future_deprecation_warning(*, reason: str, replacement: str | None, deprecation_version: str) -> None:
    """Helper function to more cleanly inform users of upcoming deprecations

    Parameters
    ----------
    reason : str
        An explanation about why this functionality has been deprecated.
    replacement : str | None
        Suggested alternative functionality to use
    deprecation_version : str
        The version of piplexed that will contain this change.
    """

    if replacement is None:
        replacement = ""

    message_parts = (reason, f"This will happen in {deprecation_version}", replacement)

    message = ". ".join(message_parts)

    warnings.warn(message.rstrip(), stacklevel=2, category=FutureWarning)


def _get_rich_console(stderr: bool = False) -> Console:  # noqa: FBT001, FBT002
    return Console(
        color_system="auto",
        width=int(TERMINAL_WIDTH) if TERMINAL_WIDTH else None,
        stderr=stderr,
    )


def rich_format_error(msg: str) -> None:
    console = _get_rich_console(stderr=True)
    console.print(Panel(msg, border_style="red", title="Error", title_align="left", width=70))


def rich_format_info(msg: str) -> None:
    console = _get_rich_console()
    console.print(Panel(msg, border_style="orange1", title="[blue]Info[/blue]", title_align="left", width=70))
