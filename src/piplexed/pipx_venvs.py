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
    python: str | None = None


def get_pipx_metadata(venv_dir: Path = PIPX_LOCAL_VENVS):
    venvs = []
    for env in venv_dir.iterdir():
        for item in env.iterdir():
            if item.suffix == ".json":
                with open(item) as f:
                    data = json.load(f)
                    pkg_data = PackageInfo(
                        name=canonicalize_name(data["main_package"]["package"]),
                        version=Version(data["main_package"]["package_version"]),
                        python=data["python_version"].split()[-1],
                    )
                    venvs.append(pkg_data)
    return venvs
