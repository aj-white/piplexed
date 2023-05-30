from packaging.version import Version

from piplexed.pipx_venvs import get_pipx_metadata
from piplexed.pipx_venvs import PackageInfo


TEST_PIPX_METADATA = """{
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


def test_get_pipx_metadata(tmp_path):
    env_dir = tmp_path / "venv"
    env_dir.mkdir()
    test_json = env_dir / "test.json"
    test_json.write_text(TEST_PIPX_METADATA)
    assert get_pipx_metadata(tmp_path) == [
        PackageInfo(name="testy-mctestface", version=Version("23.1.0"), python="3.11.2")
    ]
