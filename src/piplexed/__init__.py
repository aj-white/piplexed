# SPDX-FileCopyrightText: 2023-present Andrew White <white-aj@outlook.com>
#
# SPDX-License-Identifier: MIT
from .pipx_venvs import get_pipx_metadata  # noqa
from .pypi_info import find_outdated_packages  # noqa
from .version import VERSION

__version__ = VERSION
