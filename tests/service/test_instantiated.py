import os

import pytest

from apiron.service.base import ServiceMeta

from .. import conftest


class TestInstantiatedServices:
    @pytest.mark.parametrize("value,result", [("0", False), ("false", False), ("1", True), ("true", True)])
    def test_instantiated_services_variable_true(self, value, result):
        os.environ["APIRON_INSTANTIATED_SERVICES"] = value

        assert ServiceMeta._instantiated_services() is result

    @pytest.mark.parametrize("value", ["", "YES"])
    def test_instantiated_services_variable_other(self, value):
        os.environ["APIRON_INSTANTIATED_SERVICES"] = value

        with pytest.raises(ValueError, match="Invalid"):
            ServiceMeta._instantiated_services()

    def test_singleton_constructor_arguments(self):
        """Singleton services do not accept arguments."""
        service = conftest.singleton_service()

        with pytest.raises(TypeError, match="object is not callable"):
            service(foo="bar")

    def test_instantiated_services_constructor_arguments(self):
        """Instantiated services accept arguments."""
        service = conftest.instantiated_service(returntype="class")

        service(foo="bar")
