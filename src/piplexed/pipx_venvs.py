import json
import os
from dataclasses import dataclass
from pathlib import Path

from packaging.version import Version
from packaging.utils import canonicalize_name
from packaging.utils import NormalizedName


DEFAULT_PIPX_HOME = Path.home() / ".local/pipx"
DEFAULT_PIPX_BIN_DIR = Path.home() / ".local/bin"
PIPX_HOME = Path(os.environ.get("PIPX_HOME", DEFAULT_PIPX_HOME)).resolve()
PIPX_LOCAL_VENVS = PIPX_HOME / "venvs"


@dataclass
class PackageInfo:
    name: NormalizedName
    version: Version


def get_pipx_metadata():
    venvs = []
    for env in PIPX_LOCAL_VENVS.iterdir():
        for item in env.iterdir():
            if item.suffix == ".json":
                with open(item) as f:
                    data = json.load(f)
                    pkg_data = PackageInfo(
                        canonicalize_name(data["main_package"]["package"]),
                        Version(data["main_package"]["package_version"]),
                    )
                    venvs.append(pkg_data)
    return venvs
