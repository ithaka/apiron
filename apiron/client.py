import collections
import logging
import random
from urllib import parse

import requests
from requests import adapters
from requests.packages.urllib3.util import retry

from apiron.exceptions import NoHostsAvailableException

LOGGER = logging.getLogger(__name__)

DEFAULT_CONNECTION_TIMEOUT = 1
DEFAULT_READ_TIMEOUT = 3

DEFAULT_CONNECTION_RETRIES = 1
DEFAULT_READ_RETRIES = 1
DEFAULT_TOTAL_RETRIES = 1
DEFAULT_STATUS_CODES_TO_RETRY_ON = range(500, 600)

Timeout = collections.namedtuple('Timeout', ['connection_timeout', 'read_timeout'])

DEFAULT_TIMEOUT = Timeout(connection_timeout=DEFAULT_CONNECTION_TIMEOUT, read_timeout=DEFAULT_READ_TIMEOUT)
DEFAULT_RETRY = retry.Retry(
    total=DEFAULT_TOTAL_RETRIES,
    connect=DEFAULT_CONNECTION_RETRIES,
    read=DEFAULT_READ_RETRIES,
    status_forcelist=DEFAULT_STATUS_CODES_TO_RETRY_ON,
)


class ServiceCaller:
    """
    A class for calling :mod:`services <apiron.service.base>`
    """

    @staticmethod
    def build_url(host, path):
        """
        Builds a valid URL from a host and path which may or may not have slashes in the proper place.
        Does not conform to `IETF RFC 1808 <https://tools.ietf.org/html/rfc1808.html>`_ but instead joins the host and path as given.
        Does not append any additional slashes to the final URL; just joins the host and path properly.

        :param str host:
            An HTTP host like ``'https://awesome-api.com/v2'``
        :param str path:
            The path to an endpoint on the host like ``'/some-resource/'``
        :return:
            The properly-joined URL of host and path, e.g. ``'https://awesome-api.com/v2/some-resource/'``
        :rtype:
            str
        """
        host += '/' if not host.endswith('/') else ''
        path = path.lstrip('/')

        return parse.urljoin(host, path)

    @staticmethod
    def get_adapted_session(adapter):
        """
        Mounts an adapter capable of communication over HTTP or HTTPS to the supplied session.

        :param adapter:
            A :class:`requests.adapters.HTTPAdapter` instance
        :return:
            The adapted :class:`requests.Session` instance
        """
        session = requests.Session()
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    @staticmethod
    def get_required_headers(service, endpoint):
        """
        :param Service service:
            The service being called
        :param Endpoint endpoint:
            The endpoint being called
        :return:
            Headers required by the ``service`` and the ``endpoint`` being called
        :rtype:
            dict
        """
        headers = {}
        headers.update(service.required_headers)
        headers.update(endpoint.required_headers)
        return headers

    @staticmethod
    def choose_host(service):
        hosts = service.get_hosts()
        if not hosts:
            raise NoHostsAvailableException(service.service_name)
        return random.choice(hosts)

    @classmethod
    def build_request_object(
        cls,
        session,
        service,
        endpoint,
        method=None,
        path_kwargs=None,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        auth=None,
    ):
        host = cls.choose_host(service=service)

        path_kwargs = path_kwargs or {}
        path = endpoint.get_formatted_path(**path_kwargs)

        merged_params = endpoint.get_merged_params(params)

        headers = headers or {}
        headers.update(cls.get_required_headers(service, endpoint))

        request = requests.Request(
            method=method or endpoint.default_method,
            url=cls.build_url(host, path),
            params=merged_params,
            data=data,
            headers=headers,
            cookies=cookies,
            auth=auth,
        )

        return session.prepare_request(request)

    @classmethod
    def call(
        cls,
        service,
        endpoint,
        method=None,
        path_kwargs=None,
        session=None,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        auth=None,
        encoding=None,
        retry_spec=DEFAULT_RETRY,
        timeout_spec=DEFAULT_TIMEOUT,
        logger=None,
    ):
        """
        :param Service service:
            The service that hosts the endpoint being called
        :param Endpoint endpoint:
            The endpoint being called
        :param str method:
            The HTTP method to use for the call
        :param dict path_kwargs:
            Arguments to be formatted into the ``endpoint`` argument's ``path`` attribute
            (default ``None``)
        :param requests.Session session:
            (optional)
            An existing session, useful for making many calls in a single session
            (default ``None``)
        :param dict params:
            (optional)
            ``GET`` parameters to send to the endpoint
            (default ``None``)
        :param dict data:
            (optional)
            ``POST`` data to send to the endpoint.
            A :class:`dict` will be form-encoded, while a :class:`str` will be sent raw
            (default ``None``)
        :param dict headers:
            HTTP Headers to send to the endpoint
            (default ``None``)
        :param dict cookies:
            Cookies to send to the endpoint
            (default ``None``)
        :param auth:
            An object suitable for the :class:`requests.Request` object's ``auth`` argument
        :param str encoding:
            The codec to use when decoding the response.
            Default behavior is to have ``requests`` guess the codec.
            (default ``None``)
        :param urllib3.util.retry.Retry retry_spec:
            (optional)
            An override of the retry behavior for this call.
            (default ``Retry(total=1, connect=1, read=1, status_forcelist=[500-level status codes])``)
        :param Timeout timeout_spec:
            (optional)
            An override of the timeout behavior for this call.
            (default ``Timeout(connection_timeout=1, read_timeout=3)``)
        :param logging.Logger logger:
            (optional)
            An existing logger for logging from the proper caller for better correlation
        :return:
            The result of ``endpoint``'s :func:`format_response`
        :rtype: The type returned by ``endpoint``'s :func:`format_response`
        :raises requests.RetryError:
            if retry threshold exceeded due to bad HTTP codes (default 500 range)
        :raises requests.ConnectionError:
            if retry threshold exceeded due to connection or request timeouts
        """
        logger = logger or LOGGER

        if hasattr(endpoint, 'stub_response'):
            logger.info(
                'Stub call for endpoint defined by {}'
                .format(getattr(endpoint, 'endpoint_params', {}))
            )
            if hasattr(endpoint.stub_response, '__call__'):
                return endpoint.stub_response(
                    method=method or endpoint.default_method,
                    path_kwargs=path_kwargs,
                    params=params,
                    data=data,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                )
            else:
                return endpoint.stub_response

        managing_session = False

        if not session:
            session = cls.get_adapted_session(adapters.HTTPAdapter(max_retries=retry_spec))
            managing_session = True

        request = cls.build_request_object(
            session,
            service,
            endpoint,
            method=method or endpoint.default_method,
            path_kwargs=path_kwargs,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            auth=auth,
        )

        logger.info('{method} {url}'.format(
            method=method or endpoint.default_method,
            url=request.url,
        ))

        response = session.send(
            request,
            timeout=(timeout_spec.connection_timeout, timeout_spec.read_timeout),
            stream=getattr(endpoint, 'streaming', False),
        )

        logger.info('{status} {url}{history}'.format(
            status=response.status_code,
            url=response.url,
            history=' ({} redirect(s))'.format(len(response.history)) if response.history else '',
        ))

        if managing_session:
            session.close()

        response.raise_for_status()

        if encoding:
            response.encoding = encoding

        return endpoint.format_response(response)
