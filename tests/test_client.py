import io
from unittest import mock

import pytest

from apiron import client, NoHostsAvailableException


@pytest.fixture
def mock_response():
    response = mock.Mock()
    response.history = []
    return response


@pytest.fixture
def mock_endpoint():
    endpoint = mock.Mock()
    endpoint.required_headers = {}
    endpoint.get_formatted_path.return_value = "/foo/"
    del endpoint.stub_response
    return endpoint


@pytest.fixture
def mock_logger():
    return mock.Mock()


@mock.patch("requests.sessions.Session", autospec=True)
def test_adapt_session(mock_session):
    adapter = mock.Mock()
    mock_session.get_adapter.return_value = adapter
    adapted_session = client._adapt_session(mock_session, adapter)
    assert adapter == adapted_session.get_adapter("http://foo.com")
    assert adapter == adapted_session.get_adapter("https://foo.com")


def test_get_required_headers(mock_endpoint):
    service = mock.Mock()
    service.required_headers = {"one": "two"}
    mock_endpoint.required_headers = {"foo": "bar"}
    expected_headers = {}
    expected_headers.update(service.required_headers)
    expected_headers.update(mock_endpoint.required_headers)
    assert expected_headers == client._get_required_headers(service, mock_endpoint)


@mock.patch("apiron.client.requests.Request")
@mock.patch("apiron.client._get_required_headers")
def test_build_request_object_passes_arguments_to_request_constructor(
    mock_get_required_headers, mock_request_constructor, mock_endpoint
):
    session = mock.Mock()

    service = mock.Mock()
    service.get_hosts.return_value = ["http://host1.biz"]

    mock_endpoint.default_method = "POST"
    mock_endpoint.required_headers = {"header": "value"}
    mock_endpoint.required_params = set()

    params = {"baz": "qux"}
    mock_endpoint.get_merged_params.return_value = params
    data = "I am a data"
    files = {"file_name": io.BytesIO(b"this is a test")}
    json = {"raw": "data"}
    headers = {"Accept": "stuff"}
    cookies = {"chocolate-chip": "yes"}
    auth = mock.Mock()

    mock_get_required_headers.return_value = {"header": "value"}
    expected_headers = {}
    expected_headers.update(headers)
    expected_headers.update(mock_endpoint.required_headers)

    with mock.patch.object(session, "prepare_request") as mock_prepare_request:
        client._build_request_object(
            session,
            service,
            mock_endpoint,
            params=params,
            data=data,
            files=files,
            json=json,
            headers=headers,
            cookies=cookies,
            auth=auth,
            foo="bar",
        )

        mock_request_constructor.assert_called_once_with(
            url="http://host1.biz/foo/",
            method=mock_endpoint.default_method,
            headers=expected_headers,
            cookies=cookies,
            params=params,
            data=data,
            files=files,
            json=json,
            auth=auth,
        )

        assert 1 == mock_prepare_request.call_count


@mock.patch("apiron.client.Timeout")
@mock.patch("apiron.client._adapt_session")
@mock.patch("apiron.client._build_request_object")
@mock.patch("requests.adapters.HTTPAdapter", autospec=True)
@mock.patch("requests.Session", autospec=True)
def test_call(
    MockSession,
    MockAdapter,
    mock_build_request_object,
    mock_adapt_session,
    mock_timeout,
    mock_response,
    mock_endpoint,
    mock_logger,
):
    service = mock.Mock()
    service.get_hosts.return_value = ["http://host1.biz"]

    mock_endpoint.default_method = "GET"
    mock_endpoint.streaming = True

    request = mock.Mock()
    request.url = "http://host1.biz/foo/"
    mock_build_request_object.return_value = request

    mock_response.status_code = 200
    mock_response.url = "http://host1.biz/foo/"

    mock_session = MockSession()
    mock_session.send.return_value = mock_response
    mock_session.proxies = {}
    mock_session.auth = ()
    mock_adapt_session.return_value = mock_session

    client.call(service, mock_endpoint, timeout_spec=mock_timeout, logger=mock_logger)

    mock_adapt_session.assert_called_once_with(mock_session, MockAdapter())
    mock_session.send.assert_called_once_with(
        request,
        timeout=(mock_timeout.connection_timeout, mock_timeout.read_timeout),
        stream=mock_endpoint.streaming,
        allow_redirects=True,
        proxies=service.proxies,
    )

    mock_logger.info.assert_any_call("GET http://host1.biz/foo/")
    mock_logger.info.assert_any_call("200 http://host1.biz/foo/")

    mock_endpoint.default_method = "POST"
    request.method = "POST"

    client.call(service, mock_endpoint, session=mock_session, timeout_spec=mock_timeout, logger=mock_logger)

    mock_session.send.assert_any_call(
        request,
        timeout=(mock_timeout.connection_timeout, mock_timeout.read_timeout),
        stream=mock_endpoint.streaming,
        allow_redirects=True,
        proxies=service.proxies,
    )

    mock_logger.info.assert_any_call("GET http://host1.biz/foo/")
    mock_logger.info.assert_any_call("200 http://host1.biz/foo/")

    request.method = "PUT"

    client.call(
        service, mock_endpoint, method="PUT", session=mock_session, timeout_spec=mock_timeout, logger=mock_logger
    )

    mock_session.send.assert_any_call(
        request,
        timeout=(mock_timeout.connection_timeout, mock_timeout.read_timeout),
        stream=mock_endpoint.streaming,
        allow_redirects=True,
        proxies=service.proxies,
    )


@mock.patch("apiron.client._build_request_object")
@mock.patch("apiron.client._adapt_session")
@mock.patch("requests.Session", autospec=True)
def test_call_auth_priority(MockSession, mock_adapt_session, mock_build_request_object, mock_endpoint, mock_logger):
    service = mock.Mock()
    service.get_hosts.return_value = ["http://host1.biz"]
    service.required_headers = {}
    service.auth = ("service-user", "p455w0rd!")

    mock_session = MockSession()
    mock_session.proxies = {}
    mock_session.auth = ("session-user", "p455w0rd!")

    mock_adapt_session.return_value = mock_session

    client.call(service, mock_endpoint, auth=("direct-user", "p455w0rd!"), session=mock_session, logger=mock_logger)
    assert mock_build_request_object.call_args[1]["auth"] == ("direct-user", "p455w0rd!")

    client.call(service, mock_endpoint, session=mock_session, logger=mock_logger)
    assert mock_build_request_object.call_args[1]["auth"] == ("session-user", "p455w0rd!")

    mock_session.auth = ()
    client.call(service, mock_endpoint, logger=mock_logger)
    assert mock_build_request_object.call_args[1]["auth"] == ("service-user", "p455w0rd!")


def test_call_with_existing_session(mock_response, mock_endpoint, mock_logger):
    service = mock.Mock()
    service.get_hosts.return_value = ["http://host1.biz"]
    service.required_headers = {}

    session = mock.Mock()
    session.send.return_value = mock_response

    client.call(service, mock_endpoint, session=session, logger=mock_logger)

    assert not session.close.called


def test_call_with_explicit_encoding(mock_response, mock_endpoint, mock_logger):
    service = mock.Mock()
    service.get_hosts.return_value = ["http://host1.biz"]
    service.required_headers = {}

    session = mock.Mock()
    session.send.return_value = mock_response

    client.call(service, mock_endpoint, session=session, logger=mock_logger, encoding="FAKE-CODEC")

    assert "FAKE-CODEC" == mock_response.encoding


def test_build_request_object_raises_no_host_exception():
    service = mock.Mock()
    service.get_hosts.return_value = []

    with pytest.raises(NoHostsAvailableException):
        client._build_request_object(None, service, None)


def test_choose_host_returns_one_of_the_available_hosts():
    hosts = ["foo", "bar", "baz"]
    service = mock.Mock()
    service.get_hosts.return_value = hosts
    assert client._choose_host(service) in hosts


def test_choose_host_raises_exception_when_no_hosts_available():
    service = mock.Mock()
    service.get_hosts.return_value = []
    with pytest.raises(NoHostsAvailableException):
        client._choose_host(service)


def test_call_when_raw_response_object_requested(mock_response, mock_endpoint, mock_logger):
    service = mock.Mock()
    service.get_hosts.return_value = ["http://host1.biz"]
    service.required_headers = {}

    session = mock.Mock()
    session.send.return_value = mock_response

    response = client.call(service, mock_endpoint, session=session, logger=mock_logger, return_raw_response_object=True)

    assert response is mock_response


def test_call_when_raw_response_object_requested_on_endpoint(mock_response, mock_endpoint):
    service = mock.Mock()
    service.get_hosts.return_value = ["http://host1.biz"]
    service.required_headers = {}

    session = mock.Mock()
    session.send.return_value = mock_response

    mock_endpoint.return_raw_response_object = True

    response = client.call(service, mock_endpoint, session=session, logger=mock.Mock())

    assert response is mock_response


def test_return_raw_response_object_in_call_overrides_endpoint(mock_response, mock_endpoint):
    service = mock.Mock()
    service.get_hosts.return_value = ["http://host1.biz"]
    service.required_headers = {}

    session = mock.Mock()
    session.send.return_value = mock_response

    mock_endpoint.return_raw_response_object = False

    response = client.call(
        service,
        mock_endpoint,
        session=session,
        logger=mock.Mock(),
        return_raw_response_object=True,
    )

    assert response is mock_response


@pytest.mark.parametrize(
    "host,path,url",
    [
        ("http://biz.com", "/endpoint", "http://biz.com/endpoint"),
        ("http://biz.com/", "endpoint", "http://biz.com/endpoint"),
        ("http://biz.com/", "/endpoint", "http://biz.com/endpoint"),
        ("http://biz.com", "endpoint", "http://biz.com/endpoint"),
        ("http://biz.com/v2", "/endpoint", "http://biz.com/v2/endpoint"),
        ("http://biz.com/v2/", "endpoint", "http://biz.com/v2/endpoint"),
        ("http://biz.com/v2/", "/endpoint", "http://biz.com/v2/endpoint"),
        ("http://biz.com/v2", "endpoint", "http://biz.com/v2/endpoint"),
    ],
)
def test_build_url(host, path, url):
    assert url == client._build_url(host, path)
