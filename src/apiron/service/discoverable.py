from typing import Protocol

from apiron.service.base import ServiceBase


class Resolver(Protocol):
    @staticmethod
    def resolve(service_name: str) -> list[str]: ...


class DiscoverableService(ServiceBase):
    """
    A Service whose hosts are determined via a host resolver.
    A host resolver is any class with a :func:`resolve` method
    that takes a service name as its sole argument
    and returns a list of host names that correspond to that service.
    """

    host_resolver_class: type[Resolver]
    service_name: str

    @classmethod
    def get_hosts(cls) -> list[str]:
        return cls.host_resolver_class.resolve(cls.service_name)

    def __str__(self) -> str:
        return self.service_name

    def __repr__(self) -> str:
        klass = self.__class__
        return "{klass}(service_name={service_name}, host_resolver={host_resolver})".format(
            klass=klass.__name__, service_name=klass.service_name, host_resolver=klass.host_resolver_class.__name__
        )
