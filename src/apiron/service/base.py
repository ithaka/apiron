import os
import types
from typing import Any, Dict, List, Set

from apiron import Endpoint


class ServiceMeta(type):
    _instance: "ServiceBase"

    @property
    def required_headers(cls) -> Dict[str, str]:
        return cls().required_headers

    @classmethod
    def _instantiated_services(cls) -> bool:
        setting_variable = "APIRON_INSTANTIATED_SERVICES"
        false_values = ["0", "false"]
        true_values = ["1", "true"]
        environment_setting = os.getenv(setting_variable, "false").lower()
        if environment_setting in false_values:
            return False
        elif environment_setting in true_values:
            return True

        setting_values = false_values + true_values
        raise ValueError(
            f'Invalid {setting_variable}, "{environment_setting}"\n',
            f"{setting_variable} must be one of {setting_values}\n",
        )

    def __str__(cls) -> str:
        return str(cls())

    def __repr__(cls) -> str:
        return repr(cls())

    def __new__(cls, name, bases, namespace, **kwargs):
        klass = super().__new__(cls, name, bases, namespace, **kwargs)

        # Behave as a normal class if instantiated services are enabled or if
        # this is an apiron base class.
        if cls._instantiated_services() or klass.__module__.split(".")[:2] == ["apiron", "service"]:
            return klass

        # Singleton class.
        if not hasattr(klass, "_instance"):
            klass._instance = klass()

        # Mask declared Endpoints with bound instance methods. (singleton)
        for k, v in namespace.items():
            if isinstance(v, Endpoint):
                setattr(klass, k, types.MethodType(v, klass._instance))

        return klass._instance


class ServiceBase(metaclass=ServiceMeta):
    required_headers: Dict[str, Any] = {}
    auth = ()
    proxies: Dict[str, str] = {}
    domain: str

    def __setattr__(self, name, value):
        """Transform assigned Endpoints into bound instance methods."""
        if isinstance(value, Endpoint):
            value = types.MethodType(value, self)
        super().__setattr__(name, value)

    @property
    def endpoints(self) -> Set[Endpoint]:
        endpoints = set()
        for attr in self.__dict__.values():
            func = getattr(attr, "__func__", None)
            if isinstance(func, Endpoint):
                endpoints.add(func)
        return endpoints

    def get_hosts(self) -> List[str]:
        """
        The fully-qualified hostnames that correspond to this service.
        These are often determined by asking a load balancer or service discovery mechanism.

        :return:
            The hostname strings corresponding to this service
        :rtype:
            list
        """
        return [self.domain]


class Service(ServiceBase):
    """
    A base class for low-level services.

    A service has a domain off of which one or more endpoints stem.
    """

    @property
    def domain(self):
        return self._domain if self._domain else self.__class__.domain

    def __init__(self, domain=None, **kwargs):
        self._domain = domain
        self._kwargs = kwargs

        # Mask declared Endpoints with bound instance methods. (instantiated)
        for name, attr in self.__class__.__dict__.items():
            if isinstance(attr, Endpoint):
                setattr(self, name, types.MethodType(attr, self))

    def __str__(self) -> str:
        return self.domain

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(domain={self.domain})"
