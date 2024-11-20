from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path

from packaging.utils import canonicalize_name
from packaging.version import Version

from piplexed.venvs import PackageInfo
from piplexed.venvs import ToolType


def find_uv() -> tuple[bool, str]:
    uv_path = shutil.which("uv")
    return uv_path is not None, uv_path or "uv"


def find_uv_tool_dir(uv_path: str) -> str | None:
    # uv tool dir will return a tool directory even if one does not exist
    ret = subprocess.run([uv_path, "tool", "dir"], check=False, text=True, capture_output=True)  # noqa: S603

    if ret.returncode == 0:
        tool_dir = ret.stdout.strip()
        return tool_dir if Path(tool_dir).exists() else None

    return None


HAS_UV, UV_PATH = find_uv()

# If we can't find uv then there is no tool directory
UV_TOOL_DIR = find_uv_tool_dir(UV_PATH) if HAS_UV else None
UV_VENV_DIR = Path(UV_TOOL_DIR) if UV_TOOL_DIR is not None else None
OS_SYSTEM = platform.system()


def get_python_path(tool_venv_dir: Path, op_sys: str) -> Path:
    if op_sys == "Windows":
        return tool_venv_dir / "Scripts" / "python.exe"

    return tool_venv_dir / "bin" / "python"


def uv_tool_version(tool_venv_dir: Path, op_sys: str) -> str:
    python_path = get_python_path(tool_venv_dir, op_sys)
    script = f"from importlib.metadata import version; print(version('{tool_venv_dir.name}'))"
    ret = subprocess.run([python_path, "-c", script], check=False, text=True, capture_output=True)  # noqa: S603

    return ret.stdout.strip()


def installed_uv_tools(tool_dir: Path | None = UV_VENV_DIR, op_sys: str = OS_SYSTEM) -> list[PackageInfo]:
    def run_subprocess(cmd: str) -> str:
        try:
            result = subprocess.run([python_path, "-c", cmd], capture_output=True, text=True, check=True)  # noqa: S603
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"

    uv_packages: list[PackageInfo] = []

    if tool_dir is None:
        return uv_packages

    for env in tool_dir.iterdir():
        if not env.name.startswith("."):
            python_path = get_python_path(env, op_sys)

            package_version_cmd = f"from importlib.metadata import version; print(version('{env.name}'))"
            package_version = run_subprocess(package_version_cmd)

            python_version_cmd = "import sys; print(sys.version.split()[0])"
            python_version = run_subprocess(python_version_cmd)

            uv_data = PackageInfo(
                name=canonicalize_name(env.name),
                version=Version(package_version),
                python=python_version,
                tool=ToolType.UV,
            )

            uv_packages.append(uv_data)
    return uv_packages
