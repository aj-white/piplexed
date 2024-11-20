"""Logic for orchestrating what the cli flags do"""

from piplexed.display.print_table import print_installed_table
from piplexed.display.print_table import print_outdated_table
from piplexed.display.print_tree import print_installed_tree
from piplexed.display.print_tree import print_outdated_tree
from piplexed.pypi.pypi_info import find_most_recent_version_on_pypi
from piplexed.utils import rich_format_error
from piplexed.utils import rich_format_info
from piplexed.venvs import PackageInfo
from piplexed.venvs import ToolType
from piplexed.venvs.pipx_venvs import PIPX_LOCAL_VENVS
from piplexed.venvs.pipx_venvs import installed_pipx_tools
from piplexed.venvs.uv_venvs import HAS_UV
from piplexed.venvs.uv_venvs import UV_TOOL_DIR
from piplexed.venvs.uv_venvs import installed_uv_tools


def find_installed_tools(tool: ToolType) -> list[PackageInfo]:
    if tool == "pipx":
        venvs = installed_pipx_tools()
        if not venvs and PIPX_LOCAL_VENVS is None:
            rich_format_error("Looking for pipx tools.\nUnable to locate pipx venv directory.")
        elif not venvs:
            rich_format_info(f"No installed tools found in {PIPX_LOCAL_VENVS}")
    elif tool == "uv":
        venvs = installed_uv_tools()
        if not venvs and not HAS_UV:
            rich_format_error("Looking for uv tools.\nUnable to find uv on your path.")
        elif not venvs and HAS_UV and not UV_TOOL_DIR:
            rich_format_error(
                "Looking uv tools.\n"
                "Unable to find a uv tool directory.\nHave you installed a package using 'uv tool install [PACKAGE]' ?"
            )
    else:
        pipx_venvs = installed_pipx_tools()
        uv_venvs = installed_uv_tools()
        if not pipx_venvs:
            rich_format_info(
                f"Looking for {tool.value} tools installed with pipx and/or uv.\nUnable to find pipx venvs"
            )

        if not uv_venvs and not HAS_UV:
            rich_format_error(
                f"Looking for {tool.value} tools installed with pipx and/or uv.\nnable to find uv on your path."
            )
        if not uv_venvs and HAS_UV and not UV_TOOL_DIR:
            rich_format_info(
                f"Looking for {tool.value} tools installed with pipx and/or uv.\nUnable to find a uv tool directory."
            )

        venvs = pipx_venvs + uv_venvs

    return venvs


def print_installed_tools(tree: bool, tool: ToolType) -> None:
    venvs = find_installed_tools(tool)
    pipx_tools = sorted([pkg for pkg in venvs if pkg.tool == "pipx"], key=lambda x: x.name)
    uv_tools = sorted([pkg for pkg in venvs if pkg.tool == "uv"], key=lambda x: x.name)

    if pipx_tools and tree:
        print_installed_tree(pipx_tools, "pipx")
    elif pipx_tools:
        print_installed_table(pipx_tools, "pipx")

    if uv_tools and tree:
        print_installed_tree(uv_tools, "uv")
    elif uv_tools:
        print_installed_table(uv_tools, "uv")


def print_outdated_tools(is_prerelease: bool, tree: bool, tool: ToolType) -> None:
    venvs = find_installed_tools(tool)
    if not venvs:
        return

    packages_to_update = find_most_recent_version_on_pypi(venvs=venvs, is_prerelease=is_prerelease)
    if not packages_to_update:
        print("✨ Installed packages are all up to date ✨")
        return

    pipx_tools = sorted([pkg for pkg in packages_to_update if pkg.tool == "pipx"], key=lambda x: x.name)
    uv_tools = sorted([pkg for pkg in packages_to_update if pkg.tool == "uv"], key=lambda x: x.name)

    if pipx_tools and tree:
        print_outdated_tree(pipx_tools, "pipx")
    elif pipx_tools:
        print_outdated_table(pipx_tools, "pipx")

    if uv_tools and tree:
        print_outdated_tree(uv_tools, "uv")
    elif uv_tools:
        print_outdated_table(uv_tools, "uv")
