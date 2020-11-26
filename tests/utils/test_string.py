import time
import pytest

from utils.string import ELLIPSIS, truncate, human_join

# utils.string.truncate

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

# utils.string.human_join

def test_human_join():
    """Test utils.string.human_join."""
    assert "" == human_join([])
    assert "1" == human_join([1])
    assert "1 and 2" == human_join([1, 2])
    assert "1, 2 and 3" == human_join([1, 2, 3])
    assert "1, 2 or 3" == human_join([1, 2, 3], concatenator="or")

    assert "**1**" == human_join([1], bold=True)
    assert "`1`" == human_join([1], code=True)
    assert "**`1`**" == human_join([1], bold=True, code=True)