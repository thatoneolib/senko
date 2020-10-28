# pylint: disable=global-variable-undefined
import time
import pytest
from senko.utils.caching import cached_property


def test_cached_property():

    class Obj:
        def __init__(self, value):
            self.value = value

        @cached_property()
        def cached(self):
            return self.value

        def __repr__(self):
            return f"<Obj value={self.value}>"
    
    obj = Obj(1)
    assert obj.cached == 1
    obj.value += 1
    assert obj.cached == 1

    obj2 = Obj(2)
    assert obj2.cached == 2
    obj2.value -= 1
    assert obj2.cached == 2

@pytest.mark.sleep
def test_cached_property_ttl():

    class Obj:
        def __init__(self, value):
            self.value = value

        @cached_property(ttl=0.05)
        def cached(self):
            return self.value
    
    obj = Obj(1)
    assert obj.cached == 1
    obj.value += 1
    assert obj.cached == 1
    time.sleep(0.05)
    assert obj.cached == 2
