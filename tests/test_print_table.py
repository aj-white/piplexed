from _pytest.capture import CaptureFixture
from packaging.version import Version

from piplexed._print_table import print_list_table
from piplexed._print_table import print_outdated_table
from piplexed.pipx_venvs import PackageInfo


def test_print_table(capsys: CaptureFixture[str]):
    packages = [
        PackageInfo("A", Version("1.0.1"), python="3.11.3"),
        PackageInfo("B", Version("2.2.1"), python="3.11.3"),
    ]
    print_list_table(packages)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    assert output[0].startswith("Pip❎ Packages")
    assert output[1] == "┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓"
    assert output[2] == "┃ Package Name ┃ Pipx Version ┃ Python Version ┃"
    assert output[3] == "┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩"
    assert output[4] == "│            A │        1.0.1 │         3.11.3 │"
    assert output[5] == "│            B │        2.2.1 │         3.11.3 │"
    assert output[6] == "└──────────────┴──────────────┴────────────────┘"


def test_print_list_outdated(capsys: CaptureFixture[str]):
    packages = [
        {"package": "B", "pipx": Version("1.5.0"), "pypi": Version("1.6.0")},
        {"package": "C", "pipx": Version("2.6.0"), "pypi": Version("3.0a0")},
    ]

    print_outdated_table(packages)

    out, err = capsys.readouterr()
    assert not err
    output = [s.strip() for s in out.splitlines()]
    assert output[0] == "Pip❌ Outdated Packages"
    assert output[1] == "┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓"
    assert output[2] == "┃ Package Name ┃ Pipx Version ┃ PyPI Version ┃"
    assert output[3] == "┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩"
    assert output[4] == "│            B │        1.5.0 │        1.6.0 │"
    assert output[5] == "│            C │        2.6.0 │      3.0a0 ⚠ │"
    assert output[6] == "└──────────────┴──────────────┴──────────────┘"
