from packaging.version import Version

from piplexed.pipx_venvs import PackageInfo
from piplexed.pipx_venvs import get_pipx_metadata

TEST_PIPX_PYPI_METADATA = """{
    "injected_packages": {},
    "main_package": {
        "app_paths": [
            {
                "__Path__": "C:\\\\path\\\\to\\\\test.exe",
                "__type__": "Path"
            }
        ],
        "app_paths_of_dependencies": {},
        "apps": [
            "test.exe"
        ],
        "apps_of_dependencies": [],
        "include_apps": true,
        "include_dependencies": false,
        "package": "Testy_McTestFace",
        "package_or_url": "Testy_McTestFace",
        "package_version": "23.1.0",
        "pip_args": [],
        "suffix": ""
    },
    "pipx_metadata_version": "0.2",
    "python_version": "Python 3.11.2",
    "venv_args": []
}"""

TEST_PIPX_LOCAL_METADATA = """{
    "injected_packages": {},
    "main_package": {
        "app_paths": [
            {
                "__Path__": "C:\\\\path\\\\to\\\\test.exe",
                "__type__": "Path"
            }
        ],
        "app_paths_of_dependencies": {},
        "apps": [
            "local.exe"
        ],
        "apps_of_dependencies": [],
        "include_apps": true,
        "include_dependencies": false,
        "package": "Local_Package",
        "package_or_url": "path/to/local/wheel",
        "package_version": "23.1.0",
        "pip_args": [],
        "suffix": ""
    },
    "pipx_metadata_version": "0.3",
    "python_version": "Python 3.11.2",
    "venv_args": []
}"""


def test_get_pipx_metadata(tmp_path):
    env_dir = tmp_path / "venvs"
    env_dir.mkdir()
    pypi_package = env_dir / "pypi_package"
    pypi_package.mkdir()
    pypi_test_json = pypi_package / "test.json"
    pypi_test_json.write_text(TEST_PIPX_PYPI_METADATA)

    local_package = env_dir / "local_package"
    local_package.mkdir()
    local_test_json = local_package / "test.json"
    local_test_json.write_text(TEST_PIPX_LOCAL_METADATA)

    assert get_pipx_metadata(env_dir) == [
        PackageInfo(name="testy-mctestface", version=Version("23.1.0"), python="3.11.2"),
    ]
