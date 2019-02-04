import collections
from apiron.endpoint.endpoint import Endpoint


class JsonEndpoint(Endpoint):
    """
    An endpoint that returns :mimetype:`application/json`
    """

    def __init__(self, *args, path='/', default_method='GET', default_params=None, required_params=None, preserve_order=False):
        super().__init__(path=path, default_method=default_method, default_params=default_params, required_params=required_params)
        self.preserve_order = preserve_order

    def format_response(self, response):
        """
        Extracts JSON data from the response

        :param requests.Response response:
            The original response from :mod:`requests`
        :return:
            The response's JSON content
        :rtype:
            :class:`dict` if ``preserve_order`` is ``False``
        :rtype:
            :class:`collections.OrderedDict` if ``preserve_order`` is ``True``
        """

        return response.json(object_pairs_hook=collections.OrderedDict if self.preserve_order else None)

    @property
    def required_headers(self):
        return {'Accept': 'application/json'}
