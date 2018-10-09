import unittest

from apiron.service.discoverable import DiscoverableService


class FakeResolver:
    @staticmethod
    def resolve(service_name):
        return ['fake']


class FakeService(DiscoverableService):
    service_name = 'fake-service'
    host_resolver_class = FakeResolver


class DiscoverableServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.service = FakeService()

    def test_get_hosts_returns_hosts_from_resolver(self):
        self.assertListEqual(['fake'], self.service.get_hosts())

    def test_str_method(self):
        self.assertEqual('fake-service', str(self.service))

    def test_repr_method(self):
        self.assertEqual('FakeService(service_name=fake-service, host_resolver=FakeResolver)', repr(self.service))
