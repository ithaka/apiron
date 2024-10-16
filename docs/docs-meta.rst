####################################
Developing the apiron documentation
####################################

These docs are built using `sphinx <http://www.sphinx-doc.org/en/master/>`_.

**********
Developing
**********

If you have `tox` installed, you may build these docs by running `tox -e docs`.
Otherwise, you can follow the instructions below to manually install dependencies and build the docs.

Automated
=========

You can use the ``docs`` environment for ``tox`` to build the documentation.
With ``tox`` installed, run ``tox -e docs`` to build the HTML documentation.
After the documentation is built, you can serve the build directory, which will be located at ``.tox/docs/tmp/docs``.

Manual
======

You can also manage the documentation manually if you want more control.

Installation
------------

Use your favorite method to create a virtual environment and install the package with its extras for documentation:

.. code-block:: shell

    $ cd /path/to/apiron/
    $ pyenv virtualenv 3.9.0 apiron  # pick your favorite virtual environment tool
    $ pyenv local apiron
    (apiron) $ pip install -e .[docs]


Building
--------

You can build or rebuild the static documentation using ``make``:

.. code-block:: shell

    $ cd /path/to/apiron/docs/
    (apiron) $ make html
    Running Sphinx v1.7.4
    ...
    build succeeded.

    The HTML pages are in _build/html.

If you'd instead like to have the docs rebuilt as you're changing them,
you can watch for changes:

.. code-block:: shell

    $ cd /path/to/apiron/docs/
    (apiron) $ make watch
    [...] Serving on http://127.0.0.1:8000
    [...] Start watching changes
    [...] Start detecting changes
