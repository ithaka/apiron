import collections
import warnings
from unittest import mock

import pytest

from apiron import endpoint
from apiron.exceptions import UnfulfilledParameterException
from apiron.service.base import Service

@pytest.fixture
def service():
    class SomeService(Service):
        domain = 'http://foo.com'
    return SomeService

class TestEndpoint:
    def test_call(self, service):
        service.foo = endpoint.Endpoint()
        service.foo()

    def test_call_without_service_raises_exception(self):
        foo = endpoint.Endpoint()
        with pytest.raises(TypeError):
            foo()

    def test_default_attributes_from_constructor(self):
        foo = endpoint.Endpoint()
        assert '/' == foo.path
        assert 'GET' == foo.default_method

    def test_constructor_stores_passed_attributes(self):
        foo = endpoint.Endpoint(path='/foo/', default_method='POST')
        assert '/foo/' == foo.path
        assert 'POST' == foo.default_method

    def test_format_response(self):
        foo = endpoint.Endpoint()
        mock_response = mock.Mock()
        mock_response.text = 'foobar'
        assert 'foobar' == foo.format_response(mock_response)

    def test_required_headers(self):
        foo = endpoint.Endpoint()
        assert {} == foo.required_headers

    def test_str_method(self):
        foo = endpoint.Endpoint(path='/foo/bar/')
        assert '/foo/bar/' == str(foo)

    def test_format_path_with_correct_kwargs(self):
        foo = endpoint.Endpoint(path='/{one}/{two}/')
        path_kwargs = {'one': 'foo', 'two': 'bar'}
        assert '/foo/bar/' == foo.get_formatted_path(**path_kwargs)

    def test_format_path_with_incorrect_kwargs(self):
        foo = endpoint.Endpoint(path='/{one}/{two}/')
        path_kwargs = {'foo': 'bar'}
        with pytest.raises(KeyError):
            foo.get_formatted_path(**path_kwargs)

    def test_format_path_with_extra_kwargs(self):
        foo = endpoint.Endpoint(path='/{one}/{two}/')
        path_kwargs = {'one': 'foo', 'two': 'bar', 'three': 'not used'}
        assert '/foo/bar/' == foo.get_formatted_path(**path_kwargs)

    def test_query_parameter_in_path_generates_warning(self):
        with warnings.catch_warnings(record=True) as warning_records:
            warnings.simplefilter('always')
            foo = endpoint.Endpoint(path='/?foo=bar')
            assert 1 == len(warning_records)
            assert issubclass(warning_records[-1].category, UserWarning)

    def test_get_merged_params(self):
        foo = endpoint.JsonEndpoint(default_params={'foo': 'bar'}, required_params={'baz'})
        assert {'foo': 'bar', 'baz': 'qux'} == foo.get_merged_params({'baz': 'qux'})

    def test_get_merged_params_with_unsupplied_param(self):
        foo = endpoint.JsonEndpoint(default_params={'foo': 'bar'}, required_params={'baz'})

        with pytest.raises(UnfulfilledParameterException):
            foo.get_merged_params(None)

    def test_get_merged_params_with_empty_param(self):
        foo = endpoint.JsonEndpoint(default_params={'foo': 'bar'}, required_params={'baz'})

        with warnings.catch_warnings(record=True) as warning_records:
            warnings.simplefilter('always')
            assert {'foo': 'bar', 'baz': None} == foo.get_merged_params({'baz': None})
            assert 1 == len(warning_records)
            assert issubclass(warning_records[-1].category, RuntimeWarning)

    def test_get_merged_params_with_required_and_default_param(self):
        foo = endpoint.JsonEndpoint(default_params={'foo': 'bar'}, required_params={'foo'})
        assert {'foo': 'bar'} == foo.get_merged_params(None)


class TestJsonEndpoint:
    def test_format_response_when_unordered(self):
        foo = endpoint.JsonEndpoint()
        mock_response = mock.Mock()

        with mock.patch.object(mock_response, 'json') as mock_json:
            mock_json.return_value = {'foo': 'bar'}
            assert {'foo': 'bar'} == foo.format_response(mock_response)
            mock_json.assert_called_once_with(object_pairs_hook=None)

    def test_format_response_when_ordered(self):
        foo = endpoint.JsonEndpoint(preserve_order=True)
        mock_response = mock.Mock()

        with mock.patch.object(mock_response, 'json') as mock_json:
            mock_json.return_value = {'foo': 'bar'}
            assert {'foo': 'bar'} == foo.format_response(mock_response)
            mock_json.assert_called_once_with(object_pairs_hook=collections.OrderedDict)

    def test_required_headers(self):
        foo = endpoint.JsonEndpoint()
        assert {'Accept': 'application/json'} == foo.required_headers


class TestStreamingEndpoint:
    def test_format_response(self):
        foo = endpoint.StreamingEndpoint()
        mock_response = mock.Mock()
        assert mock_response.iter_content(chunk_size=None) == foo.format_response(mock_response)


class TestStubEndpoint:
    def test_stub_response(self):
        """
        Test initializing a stub endpoint with a stub response
        """
        stub_endpoint = endpoint.StubEndpoint(stub_response='stub response')
        assert 'stub response' == stub_endpoint.stub_response

    def test_extra_params(self):
        """
        Test initializing a stub endpoint with extra params
        """
        stub_endpoint = endpoint.StubEndpoint(
            stub_response='stub response',
            path='/some/path/',
            default_params={'param_name': 'param_val'},
            required_params={'param_name'},
        )
        expected_params = {
            'path': '/some/path/',
            'default_params': {'param_name': 'param_val'},
            'required_params': {'param_name'},
        }
        assert expected_params == stub_endpoint.endpoint_params
