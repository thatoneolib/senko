import time
import pytest

from utils.string import ELLIPSIS, truncate


@pytest.mark.parametrize(
    "string,length,expected",
    [
        ("abc", -1, ""),
        ("abc", 0, ""),
        ("abc", 1, ELLIPSIS),
        ("abc", 2, "a" + ELLIPSIS),
        ("abc", 3, "abc"),
        ("abc", 4, "abc"),
    ],
)
def test_truncate(string, length, expected):
    """Test utils.string.truncate."""
    output = truncate(string, length)
    assert output == expected