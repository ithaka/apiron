import unittest

from apiron.service.base import Service


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.service.domain = 'http://foo.com'

    def test_get_hosts_returns_domain(self):
        self.assertListEqual(['http://foo.com'], self.service.get_hosts())

    def test_str_method(self):
        self.assertEqual('http://foo.com', str(self.service))

    def test_repr_method(self):
        self.assertEqual('Service(domain=http://foo.com)', repr(self.service))

    def test_required_hosts_returns_dictionary(self):
        self.assertDictEqual({}, self.service.required_headers)
