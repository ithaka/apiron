import os

import pytest

import apiron


def instantiated_service(returntype="instance"):
    os.environ["APIRON_INSTANTIATED_SERVICES"] = "1"

    class SomeService(apiron.Service):
        pass

    if returntype == "instance":
        return SomeService(domain="http://foo.com")
    elif returntype == "class":
        return SomeService

    raise ValueError('Expected "returntype" value to be "instance" or "class".')


def singleton_service():
    os.environ["APIRON_INSTANTIATED_SERVICES"] = "0"

    class SomeService(apiron.Service):
        domain = "http://foo.com"

    return SomeService


@pytest.fixture(scope="function", params=["singleton", "instance"])
def service(request):
    if request.param == "singleton":
        yield singleton_service()
    elif request.param == "instance":
        yield instantiated_service()
    else:
        raise ValueError(f'unknown service type "{request.param}"')
