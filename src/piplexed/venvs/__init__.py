from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from packaging.utils import NormalizedName
from packaging.version import Version


class ToolType(str, Enum):
    PIPX = "pipx"
    UV = "uv"
    ALL = "all"


@dataclass
class PackageInfo:
    name: NormalizedName
    version: Version
    python: str | None = None
    latest_pypi_version: Version | None = None
    tool: ToolType = ToolType.PIPX

    def newer_pypi_version(self) -> bool:
        if self.latest_pypi_version is not None:
            return self.latest_pypi_version > self.version
        else:
            return False


__all__ = [
    "ToolType",
    "PackageInfo",
]
