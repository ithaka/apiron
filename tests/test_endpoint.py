import collections
from unittest import mock

import pytest

import apiron


@pytest.fixture
def service():
    class SomeService(apiron.Service):
        domain = "http://foo.com"

    return SomeService


@pytest.fixture
def stub_function():
    def stub_response(**kwargs):
        if kwargs.get("params") and kwargs["params"].get("param_key") == "param_value":
            return {"stub response": "stubby!"}
        else:
            return {"default": "response"}

    return stub_response


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
        with pytest.warns(UserWarning, match=r"Endpoint path \('/\?foo=bar'\) may contain query parameters"):
            _ = apiron.Endpoint(path="/?foo=bar")

    def test_get_merged_params(self):
        foo = apiron.Endpoint(default_params={"foo": "bar"}, required_params={"baz"})
        assert {"foo": "bar", "baz": "qux"} == foo.get_merged_params({"baz": "qux"})

    def test_get_merged_params_with_unsupplied_param(self):
        foo = apiron.Endpoint(default_params={"foo": "bar"}, required_params={"baz"})

        with pytest.raises(apiron.UnfulfilledParameterException):
            foo.get_merged_params()

    def test_get_merged_params_with_empty_param(self):
        foo = apiron.Endpoint(default_params={"foo": "bar"}, required_params={"baz"})
        with pytest.warns(RuntimeWarning, match="endpoint was called with empty parameters"):
            assert {"foo": "bar", "baz": None} == foo.get_merged_params({"baz": None})

    def test_get_merged_params_with_required_and_default_param(self):
        foo = apiron.Endpoint(default_params={"foo": "bar"}, required_params={"foo"})
        assert {"foo": "bar"} == foo.get_merged_params()

    def test_str_method(self):
        foo = apiron.Endpoint(path="/bar/baz")
        assert str(foo) == "/bar/baz"

    def test_repr_method(self):
        foo = apiron.Endpoint(path="/bar/baz")
        assert repr(foo) == "Endpoint(path='/bar/baz')"


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

    def test_str_method(self):
        foo = apiron.JsonEndpoint(path="/bar/baz")
        assert str(foo) == "/bar/baz"

    def test_repr_method(self):
        foo = apiron.JsonEndpoint(path="/bar/baz")
        assert repr(foo) == "JsonEndpoint(path='/bar/baz')"


class TestStreamingEndpoint:
    def test_format_response(self):
        foo = apiron.StreamingEndpoint()
        mock_response = mock.Mock()
        assert mock_response.iter_content(chunk_size=None) == foo.format_response(mock_response)

    def test_str_method(self):
        foo = apiron.StreamingEndpoint(path="/bar/baz")
        assert str(foo) == "/bar/baz"

    def test_repr_method(self):
        foo = apiron.StreamingEndpoint(path="/bar/baz")
        assert repr(foo) == "StreamingEndpoint(path='/bar/baz')"


class TestStubEndpoint:
    def test_stub_default_response(self, service):
        service.stub_endpoint = apiron.StubEndpoint()
        assert service.stub_endpoint() == {"response": "StubEndpoint(path='/')"}

    def test_call_static(self, service):
        service.stub_endpoint = apiron.StubEndpoint(stub_response="stub response")
        assert service.stub_endpoint() == "stub response"

    @pytest.mark.parametrize(
        "test_call_kwargs,expected_response",
        [({}, {"default": "response"}), ({"params": {"param_key": "param_value"}}, {"stub response": "stubby!"})],
    )
    def test_call_dynamic(self, test_call_kwargs, expected_response, service, stub_function):
        service.stub_endpoint = apiron.StubEndpoint(stub_response=stub_function)
        actual_response = service.stub_endpoint(**test_call_kwargs)
        assert actual_response == expected_response

    def test_call_without_service_raises_exception(self):
        stub_endpoint = apiron.StubEndpoint(stub_response="foo")
        with pytest.raises(TypeError):
            stub_endpoint()

    def test_str_method(self):
        foo = apiron.StubEndpoint(path="/bar/baz")
        assert str(foo) == "/bar/baz"

    def test_repr_method(self):
        foo = apiron.StubEndpoint(path="/bar/baz")
        assert repr(foo) == "StubEndpoint(path='/bar/baz')"
