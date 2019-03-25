import pytest

from apiron.service.base import Service


@pytest.fixture(scope='class')
def service():
    class SomeService(Service):
        domain = 'http://foo.com'
    return SomeService


class TestService:
    def test_get_hosts_returns_domain(self, service):
        assert ['http://foo.com'] == service.get_hosts()

    def test_str_method_on_class(self, service):
        assert 'http://foo.com' == str(service)

    def test_str_method_on_instance(self, service):
        assert 'http://foo.com' == str(service())

    def test_repr_method_on_class(self, service):
        assert 'SomeService(domain=http://foo.com)' == repr(service)

    def test_repr_method_on_instance(self, service):
        assert 'SomeService(domain=http://foo.com)' == repr(service())

    def test_required_hosts_returns_dictionary(self, service):
        assert {} == service.required_headers
