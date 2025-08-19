import pytest

from apiron import Endpoint, Service, ServiceBase


@pytest.fixture
def service():
    class SomeService(Service):
        domain = "http://foo.com"

    return SomeService


class TestServiceBase:
    def test_get_hosts_returns_empty_list_by_default(self):
        assert ServiceBase.get_hosts() == []

    def test_required_headers_returns_empty_dict_by_default(self, service):
        assert service.required_headers == {}


class TestService:
    def test_get_hosts_returns_domain(self, service):
        assert service.get_hosts() == ["http://foo.com"]

    def test_str_method_on_class(self, service):
        assert str(service) == "http://foo.com"

    def test_repr_method_on_class(self, service):
        assert repr(service) == "SomeService(domain=http://foo.com)"

    def test_required_headers_returns_empty_dict_by_default(self, service):
        assert service.required_headers == {}

    def test_endpoints_when_no_endpoints(self, service):
        assert service.endpoints == set()

    def test_endpoints_when_one_endpoint(self, service):
        foo = Endpoint(path="/foo")
        service.foo = foo
        assert service.endpoints == {foo}

    def test_endpoints_when_multiple_endpoints(self, service):
        foo = Endpoint(path="/foo")
        bar = Endpoint(path="/bar")

        service.foo = foo
        service.bar = bar

        assert service.endpoints == {foo, bar}
