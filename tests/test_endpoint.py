import collections
import unittest
import warnings
from unittest import mock

from apiron import endpoint
from apiron.exceptions import UnfulfilledParameterException


class EndpointTestCase(unittest.TestCase):
    def test_default_attributes_from_constructor(self):
        foo = endpoint.Endpoint()
        self.assertEqual('/', foo.path)
        self.assertEqual('GET', foo.default_method)

    def test_constructor_stores_passed_attributes(self):
        foo = endpoint.Endpoint(path='/foo/', default_method='POST')
        self.assertEqual('/foo/', foo.path)
        self.assertEqual('POST', foo.default_method)

    def test_format_response(self):
        foo = endpoint.Endpoint()
        mock_response = mock.Mock()
        mock_response.text = 'foobar'
        self.assertEqual('foobar', foo.format_response(mock_response))

    def test_required_headers(self):
        foo = endpoint.Endpoint()
        self.assertDictEqual({}, foo.required_headers)

    def test_str_method(self):
        foo = endpoint.Endpoint(path='/foo/bar/')
        self.assertEqual('/foo/bar/', str(foo))

    def test_format_path_with_correct_kwargs(self):
        foo = endpoint.Endpoint(path='/{one}/{two}/')
        path_kwargs = {'one': 'foo', 'two': 'bar'}
        self.assertEqual('/foo/bar/', foo.get_formatted_path(**path_kwargs))

    def test_format_path_with_incorrect_kwargs(self):
        foo = endpoint.Endpoint(path='/{one}/{two}/')
        path_kwargs = {'foo': 'bar'}
        with self.assertRaises(KeyError):
            foo.get_formatted_path(**path_kwargs)

    def test_format_path_with_extra_kwargs(self):
        foo = endpoint.Endpoint(path='/{one}/{two}/')
        path_kwargs = {'one': 'foo', 'two': 'bar', 'three': 'not used'}
        self.assertEqual('/foo/bar/', foo.get_formatted_path(**path_kwargs))

    def test_query_parameter_in_path_generates_warning(self):
        with warnings.catch_warnings(record=True) as warning_records:
            warnings.simplefilter('always')
            foo = endpoint.Endpoint(path='/?foo=bar')
            self.assertEqual(1, len(warning_records))
            self.assertTrue(issubclass(warning_records[-1].category, UserWarning))

    def test_get_merged_params(self):
        foo = endpoint.JsonEndpoint(default_params={'foo': 'bar'}, required_params={'baz'})

        self.assertDictEqual({'foo': 'bar', 'baz': 'quux'}, foo.get_merged_params({'baz': 'quux'}))

    def test_get_merged_params_with_unsupplied_param(self):
        foo = endpoint.JsonEndpoint(default_params={'foo': 'bar'}, required_params={'baz'})

        with self.assertRaises(UnfulfilledParameterException):
            foo.get_merged_params(None)

    def test_get_merged_params_with_empty_param(self):
        foo = endpoint.JsonEndpoint(default_params={'foo': 'bar'}, required_params={'baz'})

        with warnings.catch_warnings(record=True) as warning_records:
            warnings.simplefilter('always')
            self.assertDictEqual({'foo': 'bar', 'baz': None}, foo.get_merged_params({'baz': None}))
            self.assertEqual(1, len(warning_records))
            self.assertTrue(issubclass(warning_records[-1].category, RuntimeWarning))

    def test_get_merged_params_with_required_and_default_param(self):
        foo = endpoint.JsonEndpoint(default_params={'foo': 'bar'}, required_params={'foo'})

        self.assertDictEqual({'foo': 'bar'}, foo.get_merged_params(None))


class JsonEndpointTestCase(unittest.TestCase):
    def test_format_response_when_unordered(self):
        foo = endpoint.JsonEndpoint()
        mock_response = mock.Mock()

        with mock.patch.object(mock_response, 'json') as mock_json:
            mock_json.return_value = {'foo': 'bar'}
            self.assertDictEqual({'foo': 'bar'}, foo.format_response(mock_response))
            mock_json.assert_called_once_with(object_pairs_hook=None)

    def test_format_response_when_ordered(self):
        foo = endpoint.JsonEndpoint(preserve_order=True)
        mock_response = mock.Mock()

        with mock.patch.object(mock_response, 'json') as mock_json:
            mock_json.return_value = {'foo': 'bar'}
            self.assertDictEqual({'foo': 'bar'}, foo.format_response(mock_response))
            mock_json.assert_called_once_with(object_pairs_hook=collections.OrderedDict)

    def test_required_headers(self):
        foo = endpoint.JsonEndpoint()
        self.assertDictEqual({'Accept': 'application/json'}, foo.required_headers)


class StreamingEndpointTestCase(unittest.TestCase):
    def test_format_response(self):
        foo = endpoint.StreamingEndpoint()
        mock_response = mock.Mock()
        self.assertEqual(mock_response.iter_content(chunk_size=None), foo.format_response(mock_response))
