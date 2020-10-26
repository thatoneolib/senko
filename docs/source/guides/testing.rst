.. _testing:

Testing
#######

.. _pytest: https://docs.pytest.org/en/stable/contents.html

Senko comes with a test suite that uses `pytest`_ to run various unit tests
for the core library and other components that can be tested. These tests can
be found in the ``tests`` directory.

Setup
*****

Before you can start testing you must make some basic preparations. Senko's
tests require the ``pytest`` and ``pytest-asyncio`` modules to be installed.
If you have not yet installed these modules, you can do so by running
``pip install pytest pytest-asyncio``.

Some tests may require a connection to a test database. The connection is made
using the following values, as defined in the :func:`tests.conftest.database`
fixture. Please also ensure that the user has full rights to the database.

======= =========== =========== ======= ========
User    Password    Host        Port    Database
======= =========== =========== ======= ========
test    test        localhost   5432    test
======= =========== =========== ======= ========

Running Tests
*************

Tests can either be ran manually by calling ``pytest`` directly or, if you are
using Visual Studio Code, through the debug configuration or a launch profile.
Refer to the :ref:`vsc_launch_config` section for more information.

Pytest
======

To manually run pytest, navigate to the root directory of the project and call
``pytest tests``. You may also wish to add the option ``-x`` to stop test
execution when a test fails, and ``--capture=sys`` to capture any output made
to ``stdin`` and ``stdout`` to be displayed on test failure.

.. _filter: https://docs.pytest.org/en/stable/example/markers.html#marking-test-functions-and-selecting-them-for-a-run

Finally, you can filter tests using the ``-m`` option. For example, use
``-m "not (db or sleep)"`` to disable tests marked with ``db`` or ``sleep``.
For more information on how to filter tests using markers see pytest's
documentation on `marking test functions <filter>`_. 
For a list of all markers used in Senko's unit tests, refer to the 
:ref:`markers <testing_markers>` section.

.. _vsc_launch_config:

VSC Launch Configuration
========================

If you are using Visual Studio Code as your IDE, you can enable testing with
``pytest`` by adding the following to your ``settings.json``:

.. code-block:: json

    {
        "python.testing.pytestEnabled": true,
        "python.testing.pytestArgs": [
            "tests",
            "-x",
            "--capture=sys"
        ]
    }

Alternatively, you can add launch configurations for ``pytest`` by navigating to
the **Run** panel, editing ``launch.json`` and appending the following block
to the list of configurations:

.. code-block:: json

    {
        "name":"Pytest",
        "type":"python",
        "request":"launch",
        "module": "pytest",
        "console":"integratedTerminal",
        "args":[
            "tests",
            "-x",
            "--capture=sys"
        ]
    }

Creating Tests
**************

New test files must be added to the ``tests`` directory in the root directory
of the project and be prefixed with ``test_`` to be discoverable by pytest, e.g.
``test_i18n.py``. For a complete guide on how to create tests using pytest,
please refer to the 
`pytest documentation <https://docs.pytest.org/en/stable/getting-started.html#create-your-first-test>`_.

Furthermore, please mind the markers and fixtures used by Senko's unit tests
and apply them as necessary when writing new tests.

.. _testing_markers:

Markers
=======

The following markers are used when creating tests and can be used to filter
tests using the ``-m`` option when running pytest.

=========== ====================================================================
Marker      Description
=========== ====================================================================
``db``      Tests that involve a database connection.
``sleep``   Tests that involve the use of a sleep function such as
            :func:`time.sleep` or :func:`asyncio.sleep`.
=========== ====================================================================

Fixtures
========

The following fixtures are defined in ``tests/conftest.py``.

.. autofunction:: tests.conftest.database
