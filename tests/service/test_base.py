import pytest

from apiron import Service, ServiceBase


@pytest.fixture(scope="class")
def service():
    class SomeService(Service):
        domain = "http://foo.com"

    return SomeService


class TestServiceBase:
    def test_get_hosts_returns_empty_list_by_default(self):
        assert [] == ServiceBase.get_hosts()

    def test_required_headers_returns_empty_dict_by_default(self, service):
        assert {} == service.required_headers


class TestService:
    def test_get_hosts_returns_domain(self, service):
        assert ["http://foo.com"] == service.get_hosts()

    def test_str_method_on_class(self, service):
        assert "http://foo.com" == str(service)

    def test_str_method_on_instance(self, service):
        assert "http://foo.com" == str(service())

    def test_repr_method_on_class(self, service):
        assert "SomeService(domain=http://foo.com)" == repr(service)

    def test_repr_method_on_instance(self, service):
        assert "SomeService(domain=http://foo.com)" == repr(service())

    def test_required_headers_returns_empty_dict_by_default(self, service):
        assert {} == service.required_headers
