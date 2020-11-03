from senko.utils import CaseInsensitiveDict

def test_init():
    d = CaseInsensitiveDict(A=1)
    assert d["A"] == 1
    assert d["a"] == 1

    d = CaseInsensitiveDict({"A":1})
    assert d["A"] == 1
    assert d["a"] == 1

def test_set():
    d = CaseInsensitiveDict()

    d["Key"] = True
    assert d["key"]
    assert d["KEY"]

    d["KEY"] = False
    assert d["key"] == False
    assert d["KEY"] == False

def test_del():
    d = CaseInsensitiveDict()

    d["key"] = True
    del d["key"]
    assert len(d) == 0

    d["key"] = True
    del d["KEY"]
    assert len(d) == 0

def test_get():
    d = CaseInsensitiveDict()
    d["key"] = True
    assert d.get("key")

    assert d.get("missing") is None
    assert d.get("missing", True)

def test_getitem():
    d = CaseInsensitiveDict()
    d["key"] = True
    assert d["key"]
    assert d["KEY"]

def test_pop():
    d = CaseInsensitiveDict()
    d["key"] = True
    assert d.pop("key")

    d["KEY"] = True
    assert d.pop("key")

    d["KEY"] = True
    assert d.pop("KEY")

def test_setdefault():
    d = CaseInsensitiveDict()
    v = d.setdefault("KEY", True)
    assert v
    assert d["key"]

def test_update():
    a = CaseInsensitiveDict()
    b = {"ONE": 1}
    a.update(b)
    assert a.get("one") == 1

    a = CaseInsensitiveDict()
    b =  CaseInsensitiveDict({"ONE": 1})
    a.update(b)
    assert a.get("one") == 1