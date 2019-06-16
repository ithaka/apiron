#############
Upgrade guide
#############

This document will guide you through upgrading from `apiron` 2.X versions to `apiron` 3.X.


*********************************
Replacing ``ServiceCaller`` usage
*********************************

As of version 2.3.0, instantiating a service class and passing it to ``ServiceCaller.call`` is no longer necessary.
In 3.X, ``ServiceCaller`` has been removed altogether (though its behaviors are still in the :mod:`apiron.client` module).
Replace calls to ``ServiceCaller.call`` with the more semantic ``SomeService.some_endpoint``:

.. code-block:: python

    # Before
    from apiron.client import ServiceCaller
    from apiron.service.base import Service
    from apiron.endpoint import JsonEndpoint

    class GitHub(Service):
        domain = 'https://api.github.com'
        user = JsonEndpoint(path='/users/{username}')
        repo = JsonEndpoint(path='/repos/{org}/{repo}')

    GITHUB = GitHub()

    defunkt = ServiceCaller.call(GITHUB, GITHUB.user, path_kwargs={'username', 'defunkt'})


    # After
    from apiron.service.base import Service
    from apiron.endpoint import JsonEndpoint

    class GitHub(Service):
        domain = 'https://api.github.com'
        user = JsonEndpoint(path='/users/{username}')
        repo = JsonEndpoint(path='/repos/{org}/{repo}')

    defunkt = GitHub.user(path_kwargs={'username', 'defunkt'})


*******************
Simplifying imports
*******************

As of version 2.4.0, most classes are available as top-level imports from the ``apiron`` package:

.. code-block:: python

    # Before
    from apiron.service.base import Service
    from apiron.endpoint import JsonEndpoint

    # After
    from apiron import Service, JsonEndpoint


**************************************
Simplifying endpoint path placeholders
**************************************

As of version 2.5.0, ``path_kwargs`` is no longer necessary; just pass path fillers as additional keyword arguments:

.. code-block:: python

    # Before
    defunkt = GitHub.user(path_kwargs={'username', 'defunkt'})

    # After
    defunkt = GitHub.user(username='defunkt')


*******
Summary
*******

Prepare for apiron 3.X by installing apiron 2.5+ and doing the following:

- Replace ``ServiceCaller.call`` with the more direct ``SomeService.some_endpoint``
- Import classes from ``apiron`` directly
- Replace ``path_kwargs`` with direct keyword arguments
