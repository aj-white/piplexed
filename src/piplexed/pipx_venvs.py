from __future__ import annotations

import json
import platform
from dataclasses import dataclass
from pathlib import Path

from packaging.utils import NormalizedName
from packaging.utils import canonicalize_name
from packaging.version import Version
from platformdirs import user_data_path

if platform.system() == "Linux":
    DEFAULT_PIPX_HOME = Path(user_data_path("pipx"))
    FALLBACK_PIPX_HOMES = [Path.home() / ".local/pipx"]
elif platform.system() == "Windows":
    DEFAULT_PIPX_HOME = Path.home() / "pipx"
    FALLBACK_PIPX_HOMES = [Path.home() / ".local/pipx", Path(user_data_path("pipx"))]
else:
    DEFAULT_PIPX_HOME = Path.home() / ".local/pipx"
    FALLBACK_PIPX_HOMES = [Path(user_data_path("pipx"))]


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


def get_pipx_metadata(venv_dir: Path | None = PIPX_LOCAL_VENVS) -> list[PackageInfo]:
    venvs = []
    if venv_dir is None or not venv_dir.exists():
        msg = "Unable to find pipx venv installation location"
        raise FileNotFoundError(msg)
    for env in venv_dir.iterdir():
        for item in env.iterdir():
            if item.suffix == ".json":  # pragma: no branch
                with open(item) as f:
                    data = json.load(f)
                    # packages installed from pypi have the same package and package_or_url
                    if data["main_package"]["package"] == data["main_package"]["package_or_url"]:
                        pkg_data = PackageInfo(
                            name=canonicalize_name(data["main_package"]["package"]),
                            version=Version(data["main_package"]["package_version"]),
                            python=data["python_version"].split()[-1],
                        )
                        venvs.append(pkg_data)
    return venvs
