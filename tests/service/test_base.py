import pytest

from apiron.service.base import Service


@pytest.fixture(scope='class')
def service():
    service = Service()
    service.domain = 'http://foo.com'
    return service


class TestService:
    def test_get_hosts_returns_domain(self, service):
        assert ['http://foo.com'] == service.get_hosts()

    def test_str_method(self, service):
        assert 'http://foo.com' == str(service)

    def test_repr_method(self, service):
        assert 'Service(domain=http://foo.com)' == repr(service)

    def test_required_hosts_returns_dictionary(self, service):
        assert {} == service.required_headers
