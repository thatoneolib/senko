import os
import uuid

import pytest
from babel.messages.catalog import Catalog
from babel.messages.mofile import write_mo as _write_mo
from senko import Locales

# Fixtures

@pytest.fixture(scope="function")
def catalog_en():
    """
    Fixture that returns a message catalog used for testing.

    Uses the en_GB locale.
    """
    catalog = Catalog(locale="en_GB", charset="utf-8")
    catalog.add(
        "test_message",
        "test message"
    )
    catalog.add(
        "missing_message", 
        "missing message"
    )
    catalog.add(
        ("test_singular", "test_plural"),
        ("singular", "plural"),
    )

    return catalog

@pytest.fixture(scope="function")
def catalog_de():
    """
    Fixture that returns a message catalog for testing.

    Uses the de_DE locale.
    """
    catalog = Catalog(locale="de_DE", charset="utf-8")
    catalog.add(
        "test_message", 
        "Testnachricht"
    )
    catalog.add(
        ("test_singular", "test_plural"),
        ("Einzahl", "Mehrzahl"),
    )

    return catalog

def write_mo(filepath, catalog):
    with open(filepath, "wb") as fp:
        _write_mo(fp, catalog)

@pytest.fixture(scope="function")
def mo_en(tmpdir, catalog_en):
    """
    Fixture that passes a path to the .mo file of the en_GB catalog.
    """
    file = os.path.join(tmpdir, f"en_GB.{uuid.uuid4()}.mo")
    write_mo(file, catalog_en)
    return file

@pytest.fixture(scope="function")
def mo_de(tmpdir, catalog_de):
    """
    Fixture that passes a path to the .mo file of the de_DE catalog.
    """
    file = os.path.join(tmpdir, f"de_DE.{uuid.uuid4()}.mo")
    write_mo(file, catalog_de)
    return file

# Tests

def test_locales_load(mo_en):
    locales = Locales()
    locales.load(mo_en)
    assert locales.has("en_GB")

def test_locales_unload(mo_en):
    locales = Locales()
    locales.load(mo_en)
    assert locales.has("en_GB")
    locales.unload("en_GB")
    assert not locales.has("en_GB")

def test_locales_reload(mo_en, catalog_de):
    locales = Locales()

    locales.load(mo_en)
    assert locales.has("en_GB")
    locale = locales.get("en_GB")
    assert locale.gettext("test_message") == "test message"

    # Overwrite with German catalog.
    catalog_de.locale = "en_GB"
    write_mo(mo_en, catalog_de)

    locales.reload("en_GB")
    assert locales.has("en_GB")
    locale = locales.get("en_GB")
    assert locale.gettext("test_message") == "Testnachricht"

def test_locales_default(mo_en, mo_de):
    locales = Locales(default="en_GB")
    locales.load(mo_en)
    locales.load(mo_de)

    en_GB = locales.get("en_GB")
    missing_en = en_GB.gettext("missing_message")

    de_DE = locales.get("de_DE")
    missing_de = de_DE.gettext("missing_message")

    assert missing_en == missing_de

    missing = en_GB.gettext("actually missing")
    assert missing == "actually missing"