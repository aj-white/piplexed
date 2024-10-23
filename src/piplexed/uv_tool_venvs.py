from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path

from packaging.utils import canonicalize_name
from packaging.version import Version

from piplexed.pipx_venvs import PackageInfo


def find_uv_tool_dir() -> str | None:
    uv_path = shutil.which("uv")
    try:
        ret = subprocess.run([uv_path, "tool", "dir"], check=False, text=True, capture_output=True)  # noqa: S603
    except FileNotFoundError:
        return None

    if ret.returncode == 0:
        return ret.stdout.strip()
    else:
        return None


UV_VENV_DIR = Path(find_uv_tool_dir())


def uv_tool_version(tool_venv_dir: Path):
    os_system = platform.system()
    if os_system == "Windows":
        python_path = tool_venv_dir / "Scripts" / "python.exe"
    else:
        python_path = tool_venv_dir / "bin" / "python"

    script = f"from importlib.metadata import version; print(version('{tool_venv_dir.name}'))"
    ret = subprocess.run([python_path, "-c", script], check=False, text=True, capture_output=True)  # noqa: S603

    return ret.stdout.strip()


def get_installed_uv_tools(tool_dir: Path = UV_VENV_DIR):
    os_system = platform.system()

    def run_subprocess(cmd):
        try:
            result = subprocess.run([python_path, "-c", cmd], capture_output=True, text=True, check=True)  # noqa: S603
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"

    uv_packages = []
    for env in tool_dir.iterdir():
        if not env.name.startswith("."):
            if os_system == "Windows":
                python_path = env / "Scripts" / "python.exe"
            else:
                python_path = env / "bin" / "python"

            package_version_cmd = f"from importlib.metadata import version; print(version('{env.name}'))"
            package_version = run_subprocess(package_version_cmd)

            python_version_cmd = "import sys; print(sys.version.split()[0])"
            python_version = run_subprocess(python_version_cmd)

            uv_data = PackageInfo(
                name=canonicalize_name(env.name), version=Version(package_version), python=python_version, tool="uv"
            )

            uv_packages.append(uv_data)
    return uv_packages
