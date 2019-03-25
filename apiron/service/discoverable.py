from apiron.service.base import Service


class DiscoverableService(Service):
    """
    A Service whose hosts are determined via a host resolver.
    A host resolver is any class with a :func:`resolve` method
    that takes a service name as its sole argument and returns a
    list of host names that correspond to that service.
    """

    @classmethod
    def get_hosts(cls):
        return cls.host_resolver_class.resolve(cls.service_name)

    def __str__(self):
        return str(self.__class__)

    def __repr__(self):
        return repr(self.__class__)
