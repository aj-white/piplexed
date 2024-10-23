from __future__ import annotations

import json
import platform
import warnings
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from packaging.utils import NormalizedName
from packaging.utils import canonicalize_name
from packaging.version import Version
from platformdirs import user_data_path

PIPX_METADATA_VERSIONS = ["0.1", "0.2", "0.3", "0.4", "0.5"]
OS_PLATFORM = platform.system()


class ToolType(str, Enum):
    PIPX = "pipx"
    UV = "uv"
    ALL = "all"


def pipx_home_paths_for_os(platform_: str) -> tuple[Path, list[Path]]:
    if platform_ == "Linux":
        default_pipx_home = Path(user_data_path("pipx"))
        fallback_pipx_homes = [Path.home() / ".local/pipx"]
    elif platform_ == "Windows":
        default_pipx_home = Path.home() / "pipx"
        fallback_pipx_homes = [Path.home() / ".local/pipx", Path(user_data_path("pipx"))]
    else:
        default_pipx_home = Path.home() / ".local/pipx"
        fallback_pipx_homes = [Path(user_data_path("pipx"))]

    return (default_pipx_home, fallback_pipx_homes)


DEFAULT_PIPX_HOME, FALLBACK_PIPX_HOMES = pipx_home_paths_for_os(OS_PLATFORM)


def get_local_venv() -> Path | None:
    if DEFAULT_PIPX_HOME.exists():
        return DEFAULT_PIPX_HOME / "venvs"

    for fallback_dir in FALLBACK_PIPX_HOMES:
        if fallback_dir.exists():
            return fallback_dir / "venvs"

    return None


# PIPX_HOME = Path(os.environ.get("PIPX_HOME", DEFAULT_PIPX_HOME)).resolve()
PIPX_LOCAL_VENVS: Path | None = get_local_venv()


@dataclass
class PackageInfo:
    name: NormalizedName
    version: Version
    python: str | None = None
    latest_pypi_version: Version | None = None
    tool: ToolType = "pipx"

    def newer_pypi_version(self) -> bool:
        if self.latest_pypi_version is not None:
            return self.latest_pypi_version > self.version
        else:
            return False


def is_metadata_version_valid(metadata_version: str, pipx_metadata_vsn: list[str] = PIPX_METADATA_VERSIONS) -> bool:
    return metadata_version in pipx_metadata_vsn


def get_pipx_metadata(venv_dir: Path | None = PIPX_LOCAL_VENVS) -> list[PackageInfo]:
    venvs = []
    if venv_dir is None or not venv_dir.exists():
        msg = "Unable to find pipx venv installation location"
        raise FileNotFoundError(msg)
    for env in venv_dir.iterdir():
        for item in env.iterdir():
            if item.name == "pipx_metadata.json":  # pragma: no branch
                with open(item) as f:
                    data = json.load(f)
                    metadata_version = data["pipx_metadata_version"]
                    if not is_metadata_version_valid(metadata_version):
                        warnings.warn(
                            f"{metadata_version} is an unknown (and untested) pipx metadata version,"
                            "results may be inaccurate",
                            stacklevel=2,
                            category=UserWarning,
                        )
                    # packages installed from pypi have the same package and package_or_url
                    if data["main_package"]["package"] == data["main_package"]["package_or_url"]:
                        pkg_data = PackageInfo(
                            name=canonicalize_name(data["main_package"]["package"]),
                            version=Version(data["main_package"]["package_version"]),
                            python=data["python_version"].split()[-1],
                        )
                        venvs.append(pkg_data)

    return venvs
