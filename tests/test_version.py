from packaging.version import parse as parse_version
import piplexed


def test_version():
    v = parse_version(piplexed.VERSION)
    assert str(v) == piplexed.VERSION


def test_version_attribute_is_present():
    assert hasattr(piplexed, "__version__")


def test_version_attribute_is_a_string():
    assert isinstance(piplexed.__version__, str)
