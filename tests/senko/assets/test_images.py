import json
import os
import uuid

import pytest
import senko
# Constants

IMAGE = "https://cdn.discordapp.com/attachments/123456789/123456789/image.png"

# Fixtures

@pytest.fixture(scope="function")
def image_file(tmpdir):
    data = {"image":IMAGE}
    file = os.path.join(tmpdir, f"images.{uuid.uuid4()}.json")
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f)

    return file

@pytest.fixture(scope="function")
def image_lib(image_file):
    lib = senko.Images()
    lib.load_file(image_file)
    return lib

# Tests

def test_image_library_load_file(image_file):
    lib = senko.Images()
    lib.load_file(image_file)

    assert lib.length() == 1
    assert lib.has("image")

def test_image_library_load_dir(image_file):
    image_dir = os.path.dirname(image_file)
    lib = senko.Images()
    lib.load_dir(image_dir)

    assert lib.length() == 1
    assert lib.has("image")

def test_image_library_dict_properties(image_lib):
    assert image_lib.get("image") == IMAGE
    assert len(image_lib.values()) == 1
    assert len(image_lib.keys()) == 1
    assert len(image_lib.items()) == 1
    assert len(image_lib) == 1

    image_lib.clear()
    assert len(image_lib) == 0

def test_image_library_sentinel(image_lib):
    assert image_lib.get("missing") == image_lib.sentinel

def test_image_library_fallback(image_lib):
    assert image_lib.get("missing", fallback="fallback") == "fallback"

def test_image_library_missing(image_lib):
    image_lib.get("missing")
    missing = image_lib.get_missing()
    
    assert len(missing) == 1
    assert list(missing)[0] == "missing"
