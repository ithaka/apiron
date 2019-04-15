##############
Advanced usage
##############

`httpbin.org <https://httpbin.org>`_ is a great testing tool
for various situations you may run into when interacting with RESTful services.
Let's define a :class:`Service <apiron.service.base.Service>` that points at `httpbin.org <https://httpbin.org>`_
and hook up a few interesting endpoints.

*********************
Service and endpoints
*********************

.. code-block:: python

    # test_service.py
    from apiron import Endpoint, JsonEndpoint, Service, StreamingEndpoint

    class HttpBin(Service):
        domain = 'https://httpbin.org'

        getter = JsonEndpoint(path='/get')
        poster = JsonEndpoint(path='/post', default_method='POST')
        status = Endpoint(path='/status/{status_code}/')
        anything = JsonEndpoint(path='/anything/{anything}')
        slow = JsonEndpoint(path='/delay/5')
        streamer = StreamingEndpoint(path='/stream/{num_lines}')


**********************
Using all the features
**********************

.. code-block:: python

    import requests

    from apiron import Timeout

    from test_service import HttpBin

    # A normal old GET call
    HttpBin.getter(params={'foo': 'bar'})

    # A normal old POST call
    HttpBin.poster(data={'foo': 'bar'})

    # A GET call with parameters formatted into the path
    HttpBin.anything(anything=42)

    # A GET call with a 500 response, raises RetryError since we successfully tried but got a bad response
    try:
        HttpBin.status(status_code=500)
    except requests.exceptions.RetryError:
        pass

    # A GET call to a slow endpoint, raises ConnectionError since our connection failed
    try:
        HttpBin.slow()
    except requests.exceptions.ConnectionError:
        pass

    # A GET call to a slow endpoint with a longer timeout
    HttpBin.slow(
        timeout_spec=Timeout(connection_timeout=1, read_timeout=6)
    )

    # A streaming response
    response = HttpBin.streamer(num_lines=20)
    for chunk in response:
        print(chunk)


*****************
Service discovery
*****************

You may want to interact with a service whose name is known but whose hosts are resolved via another application.
Here is an example where the resolver application always resolves to ``https://www.google.com`` for the host.

.. code-block:: python

    from apiron import DiscoverableService

    class Eureka:
        @staticmethod
        def resolve(service_name):
            hosts = ...  # get host list from Eureka

    class AuthenticationService(DiscoverableService):
        service_name = 'authentication-service'
        host_resolver_class = Eureka

        auth = Endpoint(path='/auth')


    response = AuthenticationService.auth(data={'user': 'Gandalf', 'password': 'Mellon'})

An application may wish to use a load balancer application
or a more complex service discovery mechanism (like Netflix's `Eureka <https://github.com/Netflix/eureka>`_)
to resolve the hostnames of a given service.


********************
Workflow consistency
********************

It's common to have an existing :class:`requests.Session` object you'd like to use to make additional requests.
This is enabled in ``apiron`` with the ``session`` argument to an endpoint call.
The passed in session object will be used to send the request.
This is useful for workflows where cookies or other information need to persist across multiple calls.

It's often more useful in logs to know which module initiated the code doing the logging.
``apiron`` allows for an existing logger object to be passed to an endpoint call using the ``logger`` argument
so that logs will indicate the caller module rather than :mod:`apiron.client`.
