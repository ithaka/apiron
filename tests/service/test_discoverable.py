import pytest

from apiron.service.discoverable import DiscoverableService


class FakeResolver:
    @staticmethod
    def resolve(service_name):
        return ['fake']


class FakeService(DiscoverableService):
    service_name = 'fake-service'
    host_resolver_class = FakeResolver


@pytest.fixture(scope='class')
def service():
    return FakeService


class TestDiscoverableService:
    def test_get_hosts_returns_hosts_from_resolver(self, service):
        assert ['fake'] == service.get_hosts()

    def test_str_method_on_class(self, service):
        assert 'fake-service' == str(service)

    def test_str_method_on_instance(self, service):
        assert 'fake-service' == str(service())

    def test_repr_method_on_class(self, service):
        assert 'FakeService(service_name=fake-service, host_resolver=FakeResolver)' == repr(service)

    def test_repr_method_on_instance(self, service):
        assert 'FakeService(service_name=fake-service, host_resolver=FakeResolver)' == repr(service())
