from typing import Any

from apiron import Endpoint


class ServiceMeta(type):
    @property
    def required_headers(cls) -> dict[str, str]:
        return cls().required_headers

    @property
    def endpoints(cls) -> set[Endpoint]:
        return {attr for attr_name, attr in cls.__dict__.items() if isinstance(attr, Endpoint)}

    def __str__(cls) -> str:
        return str(cls())

    def __repr__(cls) -> str:
        return repr(cls())


class ServiceBase(metaclass=ServiceMeta):
    required_headers: dict[str, Any] = {}
    auth = ()
    proxies: dict[str, str] = {}

    @classmethod
    def get_hosts(cls) -> list[str]:
        """
        The fully-qualified hostnames that correspond to this service.
        These are often determined by asking a load balancer or service discovery mechanism.

        :return:
            The hostname strings corresponding to this service
        :rtype:
            list
        """
        return []


class Service(ServiceBase):
    """
    A base class for low-level services.

    A service has a domain off of which one or more endpoints stem.
    """

    domain: str

    @classmethod
    def get_hosts(cls) -> list[str]:
        """
        The fully-qualified hostnames that correspond to this service.
        These are often determined by asking a load balancer or service discovery mechanism.

        :return:
            The hostname strings corresponding to this service
        :rtype:
            list
        """
        return [cls.domain]

    def __str__(self) -> str:
        return getattr(self.__class__, "domain", "UNKNOWN")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(domain={self.__class__.domain})"
