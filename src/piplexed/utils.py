from __future__ import annotations

import warnings


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
