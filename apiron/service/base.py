from functools import partial

from apiron.client import ServiceCaller
from apiron.endpoint import Endpoint


class ServiceMeta(type):
    @property
    def required_headers(cls):
        return cls().required_headers

    def __getattribute__(cls, *args):
        attribute = type.__getattribute__(cls, *args)
        if isinstance(attribute, Endpoint):
            attribute.callable = partial(ServiceCaller.call, cls, attribute)
        return attribute

    def __str__(cls):
        service_name = getattr(cls, 'service_name', None)
        return service_name or cls.domain

    def __repr__(cls):
        if hasattr(cls, 'service_name'):
            return '{klass}(service_name={service_name}, host_resolver={host_resolver})'.format(
                klass=cls.__name__,
                service_name=cls.service_name,
                host_resolver=cls.host_resolver_class.__name__,
            )
        else:
            return '{klass}(domain={domain})'.format(klass=cls.__name__, domain=cls.domain)


class Service(metaclass=ServiceMeta):
    """
    A base class for low-level services.

    A service has a domain off of which one or more endpoints stem.
    """

    required_headers = {}

    @classmethod
    def get_hosts(cls):
        """
        The fully-qualified hostnames that correspond to this service.
        These are often determined by asking a load balancer or service discovery mechanism.

        :return:
            The hostname strings corresponding to this service
        :rtype:
            list
        """
        return [cls.domain]

    def __str__(self):
        return str(self.__class__)

    def __repr__(self):
        return repr(self.__class__)
