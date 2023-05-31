from _pytest.capture import CaptureFixture
from packaging.version import Version

from piplexed._print_tree import print_list_outdated
from piplexed._print_tree import print_list_tree
from piplexed.pipx_venvs import PackageInfo


def test_print_list(capsys: CaptureFixture[str]):
    packages = [
        PackageInfo("A", Version("1.0.1"), python="3.11.3"),
        PackageInfo("B", Version("2.2.1"), python="3.11.3"),
    ]
    print_list_tree(packages)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    assert output[0].startswith("Pip❎ Packages")
    assert output[1] == "├── A"
    assert output[2] == "│   ├── version - 1.0.1"
    assert output[3] == "│   └── python - 3.11.3"


def test_print_list_outdated(capsys: CaptureFixture[str]):
    packages = [
        {"package": "B", "pipx": Version("1.5.0"), "pypi": Version("1.6.0")},
        {"package": "C", "pipx": Version("2.6.0"), "pypi": Version("3.0a0")},
    ]

    print_list_outdated(packages)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    print(out)
    assert output[0] == "Pip❌ Outdated Packages"
    assert output[1] == "├── B"
    assert output[2] == "│   ├── pipx version - 1.5.0"
    assert output[3] == "│   └── PyPI version - 1.6.0"
    assert output[4] == "└── C"
    assert output[5] == "├── pipx version - 2.6.0"
    assert output[6] == "└── PyPI version - 3.0a0 ⚠"
