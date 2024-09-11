import warnings
from typing import Optional


def future_deprecation_warning(*, reason: str, replacement: Optional[str], deprecation_version: str) -> None:  # noqa: UP007
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
