import logging
import warnings

from apiron.exceptions import UnfulfilledParameterException


LOGGER = logging.getLogger(__name__)


class Endpoint:
    """
    A basic service endpoint that responds with the default ``Content-Type`` for that endpoint
    """

    def __call__(self, *args, **kwargs):
        """
        Used to provide syntax sugar on top of :func:`apiron.client.ServiceCaller.call`.
        The callable attribute is set dynamically by the :class:`Service` subclass this endpoint is a part of.
        Arguments are identical to those of :func:`apiron.client.ServiceCaller.call`
        """
        if hasattr(self, 'callable'):
            return self.callable(*args, **kwargs)
        else:
            raise TypeError('Endpoints are only callable in conjunction with a Service class.')

    def __init__(self, path='/', default_method='GET', default_params=None, required_params=None):
        """
        :param str path:
            The URL path for this endpoint, without the protocol or domain
        :param str default_method:
            (Default ``'GET'``)
            The default method to use when calling this endpoint.
        :param dict default_params:
            The default parameters to use when calling this endpoint.
            Useful when an endpoint always or most often needs a base set of parameters supplied.
        :param required_params:
            An iterable of required parameter names.
            Calling an endpoint without its required parameters raises an exception.
        """
        self.default_method = default_method

        if '?' in path:
            warnings.warn(
                'Endpoint path may contain query parameters. '
                'Use the default_params or required_params attributes in the initialization of this endpoint, '
                'or the params argument when calling the endpoint instead.'.format(path),
                stacklevel=3,
            )

        self.path = path
        self.default_params = default_params or {}
        self.required_params = required_params or set()

    def format_response(self, response):
        """
        Extracts the appropriate type of response data from a :class:`requests.Response` object

        :param requests.Response response:
            The original response from :mod:`requests`
        :return:
            The response's text content
        :rtype:
            str
        """
        return response.text

    @property
    def required_headers(self):
        """
        Generates the headers that must be sent to this endpoint based on its attributes

        :return:
            Header name, header value pairs
        :rtype:
            dict
        """
        return {}

    def get_formatted_path(self, **kwargs):
        """
        Format this endpoint's path with the supplied keyword arguments

        :return:
            The fully-formatted path
        :rtype:
            str
        """
        return self.path.format(**kwargs)

    def get_merged_params(self, supplied_params=None):
        """
        Merge this endpoint's default parameters with the supplied parameters

        :param dict supplied_params:
            A dictionary of query parameter, value pairs
        :return:
            A dictionary of this endpoint's default parameters, merged with the supplied parameters.
            Any default parameters which have a value supplied are overridden.
        :rtype:
            dict
        :raises apiron.exceptions.UnfulfilledParameterException:
            When a required parameter for this endpoint is not a default param and is not supplied by the caller
        """
        supplied_params = supplied_params or {}

        empty_params = {
            param: supplied_params[param]
            for param in supplied_params
            if supplied_params[param] in (None, '')
        }
        if empty_params:
            warnings.warn(
                'The {path} endpoint '
                'was called with empty parameters: {empty_params}'.format(
                    path=self.path,
                    empty_params=empty_params,
                ),
                RuntimeWarning,
                stacklevel=4,
            )

        unfulfilled_params = {
            param
            for param in self.required_params
            if param not in supplied_params
            and param not in self.default_params
        }

        if unfulfilled_params:
            raise UnfulfilledParameterException(
                self.path,
                unfulfilled_params,
            )

        merged_params = self.default_params.copy()
        merged_params.update(supplied_params)
        return merged_params

    def __str__(self):
        return self.path
