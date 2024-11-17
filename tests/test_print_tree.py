from _pytest.capture import CaptureFixture
from packaging.version import Version

from piplexed.display.print_tree import print_installed_tree
from piplexed.display.print_tree import print_outdated_tree
from piplexed.venvs.pipx_venvs import PackageInfo


def test_print_installed_tree(capsys: CaptureFixture[str]):
    packages = [
        PackageInfo("A", Version("1.0.1"), python="3.11.3"),
        PackageInfo("B", Version("2.2.1"), python="3.11.3"),
    ]
    print_installed_tree(packages, "pipx")

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    assert output[0].startswith("PIPX Packages")
    assert output[1] == "├── A"
    assert output[2] == "│   ├── version - 1.0.1"
    assert output[3] == "│   └── python - 3.11.3"


def test_print_outdated_tree(capsys: CaptureFixture[str]):
    packages = [
        PackageInfo("B", Version("1.5.0"), python="3.11.3", latest_pypi_version=Version("1.6.0")),
        PackageInfo("C", Version("2.6.0"), python="3.11.3", latest_pypi_version=Version("3.0a.0")),
    ]

    print_outdated_tree(packages, "pipx")

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    print(out)
    assert output[0] == "PIPX Outdated Packages"
    assert output[1] == "├── B"
    assert output[2] == "│   ├── installed version - 1.5.0"
    assert output[3] == "│   └── PyPI version - 1.6.0"
    assert output[4] == "└── C"
    assert output[5] == "├── installed version - 2.6.0"
    assert output[6] == "└── PyPI version - 3.0a0 ⚠"
