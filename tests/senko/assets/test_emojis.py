import json
import os
import uuid

import pytest
import senko

# Constants

BOOK_EMOJI = "\N{BOOK}"
STATIC_EMOJI = "<:static:123456789123456789>"
ANIMATED_EMOJI = "<a:animated:123456789123456789>"

# Fixtures

@pytest.fixture(scope="function")
def emoji_file(tmpdir):
    data = {
        "book": BOOK_EMOJI,
        "static": STATIC_EMOJI,
        "animated": ANIMATED_EMOJI,
    }
    file = os.path.join(tmpdir, f"emojis.{uuid.uuid4()}.json")
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f)

    return file

@pytest.fixture(scope="function")
def emoji_lib(emoji_file):
    lib = senko.Emojis()
    lib.load_file(emoji_file)
    return lib

# Tests

def test_emoji_library_load_file(emoji_file):
    library = senko.Emojis()
    library.load_file(emoji_file)

    assert library.length() == 3
    assert library.has("book")
    assert library.has("static")
    assert library.has("animated")

def test_emoji_library_load_dir(emoji_file):
    emoji_dir = os.path.dirname(emoji_file)
    library = senko.Emojis()
    library.load_dir(emoji_dir)

    assert library.length() == 3
    assert library.has("book")
    assert library.has("static")
    assert library.has("animated")

def test_emoji_library_dict_properties(emoji_lib):
    lib = emoji_lib

    book = lib.get("book")
    assert book == lib["book"]
    assert len(lib.values()) == 3
    assert len(lib.keys()) == 3
    assert len(lib.items()) == 3
    assert len(lib) == 3

    lib.clear()
    assert len(lib) == 0

def test_emoji_library_sentinel(emoji_lib):
    assert emoji_lib.get("missing") == emoji_lib.sentinel

def test_emoji_library_fallback(emoji_lib):
    assert emoji_lib.get("missing", fallback="fallback") == "fallback"

def test_emoji_library_missing(emoji_lib):
    emoji_lib.get("missing")

    missing = emoji_lib.get_missing()
    assert len(missing) == 1
    assert list(missing)[0] == "missing"

    emoji_lib.clear_missing()

    missing = emoji_lib.get_missing()
    assert len(missing) == 0

def test_emoji_library_unicode(emoji_lib):
    book = emoji_lib.get("book")

    assert book.name == BOOK_EMOJI
    assert book.id == None
    assert book.animated == False

def test_emoji_library_static(emoji_lib):
    static = emoji_lib.get("static")

    assert static.name == "static"
    assert static.id == 123456789123456789
    assert static.animated == False

def test_emoji_library_animated(emoji_lib):
    animated = emoji_lib.get("animated")

    assert animated.name == "animated"
    assert animated.id == 123456789123456789
    assert animated.animated == True

def test_emoji_library_format(emoji_lib):
    assert emoji_lib.format("{e:book}") == BOOK_EMOJI

    string = emoji_lib.format("{e:book} {0} {1} {key}", 1, 2, key="key")
    assert string == f"{BOOK_EMOJI} 1 2 key"
