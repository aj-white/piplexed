from unittest.mock import patch

import pytest

from piplexed.utils import future_deprecation_warning


def test_future_deprecation_warning_with_replacement():
    with patch("warnings.warn") as mock_warn:
        future_deprecation_warning(
            reason="Functionality is being deprecated",
            replacement="Use the new_function() instead",
            deprecation_version="2.0.0",
        )
        mock_warn.assert_called_once_with(
            "Functionality is being deprecated. This will happen in 2.0.0. Use the new_function() instead",
            stacklevel=2,
            category=FutureWarning,
        )


def test_future_deprecation_warning_without_replacement():
    with patch("warnings.warn") as mock_warn:
        future_deprecation_warning(
            reason="Functionality is being deprecated", replacement=None, deprecation_version="2.0.0"
        )
        mock_warn.assert_called_once_with(
            "Functionality is being deprecated. This will happen in 2.0.0.", stacklevel=2, category=FutureWarning
        )


def test_future_deprecation_warning_empty_replacement():
    with patch("warnings.warn") as mock_warn:
        future_deprecation_warning(
            reason="Functionality is being deprecated", replacement="", deprecation_version="2.0.0"
        )
        mock_warn.assert_called_once_with(
            "Functionality is being deprecated. This will happen in 2.0.0.", stacklevel=2, category=FutureWarning
        )


def test_future_deprecation_warning_with_non_string_replacement():
    with pytest.raises(TypeError):
        future_deprecation_warning(
            reason="Functionality is being deprecated", replacement=1234, deprecation_version="2.0.0"
        )
