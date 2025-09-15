import collections
from collections.abc import Iterable
from typing import Any

from urllib3.util import retry

from apiron import Timeout
from apiron.endpoint.endpoint import Endpoint


class JsonEndpoint(Endpoint):
    """
    An endpoint that returns :mimetype:`application/json`
    """

    def __init__(
        self,
        *args,
        path: str = "/",
        default_method: str = "GET",
        default_params: dict[str, Any] | None = None,
        required_params: Iterable[str] | None = None,
        preserve_order: bool = False,
        return_raw_response_object: bool = False,
        timeout_spec: Timeout | None = None,
        retry_spec: retry.Retry | None = None,
    ):
        super().__init__(
            path=path,
            default_method=default_method,
            default_params=default_params,
            required_params=required_params,
            return_raw_response_object=return_raw_response_object,
            timeout_spec=timeout_spec,
            retry_spec=retry_spec,
        )
        self.preserve_order = preserve_order

    def format_response(self, response) -> dict[str, Any]:
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
    def required_headers(self) -> dict[str, str]:
        return {"Accept": "application/json"}
