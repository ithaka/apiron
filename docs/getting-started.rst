###############
Getting started
###############

The goal of ``apiron`` is to get you up and running quickly,
consuming a service with little initial configuration
while allowing for granular customization.
The declarative nature of this setup makes the shape of services and their endpoints more obvious
than placing those details in one-off calls.

The minimum possible configuration requires a bit of information about the service.


******************
Defining a service
******************

A service definition requires a domain
and one or more endpoints with which to interact:

.. code-block:: python

    from apiron import JsonEndpoint, Service

    class GitHub(Service):
        domain = 'https://api.github.com'
        user = JsonEndpoint(path='/users/{username}')
        repo = JsonEndpoint(path='/repos/{org}/{repo}')


**************************
Interacting with a service
**************************

Once your service definition is in place, you can interact with its endpoints
in an SDK-like manner:

.. code-block:: python

    response = GitHub.user(username='defunkt')
    # {"name": "Chris Wanstrath", ...}

    response = GitHub.repo(org='github', repo='hub')
    # {"description": "hub helps you win at git.", ...}


**********
Next steps
**********

Now that you're a seasoned pro, explore the :doc:`advanced usage <advanced-usage>`!
