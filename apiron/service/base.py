from apiron import Endpoint


class ServiceMeta(type):
    @property
    def required_headers(cls):
        return cls().required_headers

    @property
    def endpoints(cls):
        return {attr for attr_name, attr in cls.__dict__.items() if isinstance(attr, Endpoint)}

    def __str__(cls):
        return str(cls())

    def __repr__(cls):
        return repr(cls())


class ServiceBase(metaclass=ServiceMeta):
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
        return []


class Service(ServiceBase):
    """
    A base class for low-level services.

    A service has a domain off of which one or more endpoints stem.
    """

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
        return self.__class__.domain

    def __repr__(self):
        return "{klass}(domain={domain})".format(klass=self.__class__.__name__, domain=self.__class__.domain)
