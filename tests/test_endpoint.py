import collections
from unittest import mock

import pytest

import apiron
from apiron import ServiceCaller


@pytest.fixture
def service():
    class SomeService(apiron.Service):
        domain = "http://foo.com"

    return SomeService


class TestEndpoint:
    def test_call(self, service):
        service.foo = apiron.Endpoint()
        service.foo()

    def test_call_without_service_raises_exception(self):
        foo = apiron.Endpoint()
        with pytest.raises(TypeError):
            foo()

    def test_default_attributes_from_constructor(self):
        foo = apiron.Endpoint()
        assert "/" == foo.path
        assert "GET" == foo.default_method

    def test_constructor_stores_passed_attributes(self):
        foo = apiron.Endpoint(path="/foo/", default_method="POST")
        assert "/foo/" == foo.path
        assert "POST" == foo.default_method

    def test_format_response(self):
        foo = apiron.Endpoint()
        mock_response = mock.Mock()
        mock_response.text = "foobar"
        assert "foobar" == foo.format_response(mock_response)

    def test_required_headers(self):
        foo = apiron.Endpoint()
        assert {} == foo.required_headers

    def test_str_method(self):
        foo = apiron.Endpoint(path="/foo/bar/")
        assert "/foo/bar/" == str(foo)

    def test_path_placeholders_when_none_present(self):
        foo = apiron.Endpoint()
        assert [] == foo.path_placeholders

    def test_path_placeholders_when_present(self):
        foo = apiron.Endpoint(path="/foo/{one}/{two}")
        assert ["one", "two"] == foo.path_placeholders

    def test_format_path_with_correct_kwargs(self):
        foo = apiron.Endpoint(path="/{one}/{two}/")
        path_kwargs = {"one": "foo", "two": "bar"}
        assert "/foo/bar/" == foo.get_formatted_path(**path_kwargs)

    def test_format_path_with_incorrect_kwargs(self):
        foo = apiron.Endpoint(path="/{one}/{two}/")
        path_kwargs = {"foo": "bar"}
        with pytest.warns(RuntimeWarning, match="An unknown path kwarg was supplied"):
            with pytest.raises(KeyError):
                foo.get_formatted_path(**path_kwargs)

    def test_format_path_with_extra_kwargs(self):
        foo = apiron.Endpoint(path="/{one}/{two}/")
        path_kwargs = {"one": "foo", "two": "bar", "three": "not used"}
        with pytest.warns(RuntimeWarning, match="An unknown path kwarg was supplied"):
            assert "/foo/bar/" == foo.get_formatted_path(**path_kwargs)

    def test_query_parameter_in_path_generates_warning(self):
        with pytest.warns(UserWarning, match="Endpoint path may contain query parameters"):
            _ = apiron.Endpoint(path="/?foo=bar")

    def test_get_merged_params(self):
        foo = apiron.JsonEndpoint(default_params={"foo": "bar"}, required_params={"baz"})
        assert {"foo": "bar", "baz": "qux"} == foo.get_merged_params({"baz": "qux"})

    def test_get_merged_params_with_unsupplied_param(self):
        foo = apiron.JsonEndpoint(default_params={"foo": "bar"}, required_params={"baz"})

        with pytest.raises(apiron.UnfulfilledParameterException):
            foo.get_merged_params()

    def test_get_merged_params_with_empty_param(self):
        foo = apiron.JsonEndpoint(default_params={"foo": "bar"}, required_params={"baz"})
        with pytest.warns(RuntimeWarning, match="endpoint was called with empty parameters"):
            assert {"foo": "bar", "baz": None} == foo.get_merged_params({"baz": None})

    def test_get_merged_params_with_required_and_default_param(self):
        foo = apiron.JsonEndpoint(default_params={"foo": "bar"}, required_params={"foo"})
        assert {"foo": "bar"} == foo.get_merged_params()

    @mock.patch("apiron.client.requests.Session.send")
    def test_using_path_kwargs_produces_warning(self, mock_send, service):
        service.foo = apiron.Endpoint(path="/foo/{one}")
        with pytest.warns(RuntimeWarning, match="path_kwargs is no longer necessary"):
            _ = service.foo(path_kwargs={"one": "bar"})

    @mock.patch("apiron.client.Timeout")
    @mock.patch("requests.Session", autospec=True)
    def test_legacy_endpoint_usage_with_instantiated_service(self, MockSession, mock_timeout, service):
        service.foo = apiron.Endpoint(path="/foo/")
        instantiated_service = service()

        mock_logger = mock.Mock()
        request = mock.Mock()
        request.url = "http://host1.biz/foo/"

        ServiceCaller.call(
            instantiated_service, instantiated_service.foo, timeout_spec=mock_timeout, logger=mock_logger
        )


class TestJsonEndpoint:
    def test_format_response_when_unordered(self):
        foo = apiron.JsonEndpoint()
        mock_response = mock.Mock()

        with mock.patch.object(mock_response, "json") as mock_json:
            mock_json.return_value = {"foo": "bar"}
            assert {"foo": "bar"} == foo.format_response(mock_response)
            mock_json.assert_called_once_with(object_pairs_hook=None)

    def test_format_response_when_ordered(self):
        foo = apiron.JsonEndpoint(preserve_order=True)
        mock_response = mock.Mock()

        with mock.patch.object(mock_response, "json") as mock_json:
            mock_json.return_value = {"foo": "bar"}
            assert {"foo": "bar"} == foo.format_response(mock_response)
            mock_json.assert_called_once_with(object_pairs_hook=collections.OrderedDict)

    def test_required_headers(self):
        foo = apiron.JsonEndpoint()
        assert {"Accept": "application/json"} == foo.required_headers


class TestStreamingEndpoint:
    def test_format_response(self):
        foo = apiron.StreamingEndpoint()
        mock_response = mock.Mock()
        assert mock_response.iter_content(chunk_size=None) == foo.format_response(mock_response)


class TestStubEndpoint:
    def test_stub_response(self):
        """
        Test initializing a stub endpoint with a stub response
        """
        stub_endpoint = apiron.StubEndpoint(stub_response="stub response")
        assert "stub response" == stub_endpoint.stub_response

    def test_extra_params(self):
        """
        Test initializing a stub endpoint with extra params
        """
        stub_endpoint = apiron.StubEndpoint(
            stub_response="stub response",
            path="/some/path/",
            default_params={"param_name": "param_val"},
            required_params={"param_name"},
            arbitrary_kwarg="foo",
        )
        expected_params = {
            "path": "/some/path/",
            "default_params": {"param_name": "param_val"},
            "required_params": {"param_name"},
            "arbitrary_kwarg": "foo",
        }
        assert expected_params == stub_endpoint.endpoint_params

    def test_call_static(self, service):
        """
        Test calling a ``StubEndpoint`` with a static response
        """
        service.stub_endpoint = apiron.StubEndpoint(stub_response="stub response")
        actual_response = service.stub_endpoint()
        expected_response = "stub response"
        assert actual_response == expected_response

    def test_call_dynamic(self, service):
        """
        Test calling a StubEndpoint with a dynamic response
        """

        def _test_case(call_kwargs, expected_response):
            def stub_response(**kwargs):
                if kwargs.get("params") and kwargs["params"].get("param_key") == "param_value":
                    return {"stub response": "for param_key=param_value"}
                else:
                    return {"default": "response"}

            service.stub_endpoint = apiron.StubEndpoint(stub_response=stub_response)
            actual_response = service.stub_endpoint(**call_kwargs)
            assert actual_response == expected_response

        _test_case(call_kwargs={}, expected_response={"default": "response"})
        _test_case(
            call_kwargs={"params": {"param_key": "param_value"}},
            expected_response={"stub response": "for param_key=param_value"},
        )

    def test_call_without_service_raises_exception(self):
        stub_endpoint = apiron.StubEndpoint(stub_response="foo")
        with pytest.raises(TypeError):
            stub_endpoint()
