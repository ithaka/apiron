from functools import partial, update_wrapper

from apiron import ServiceCaller


class StubEndpoint:
    """
    A stub endpoint designed to return a pre-baked response

    The intent is to allow for a service to be implemented
    before the endpoint is complete.
    """

    def __get__(self, instance, owner):
        caller = partial(ServiceCaller.call, owner, self)
        update_wrapper(caller, ServiceCaller.call)
        return caller

    def __call__(self):
        raise TypeError("Endpoints are only callable in conjunction with a Service class.")

    def __init__(self, stub_response=None, **kwargs):
        """
        :param stub_response:
            A pre-baked response or response-determining function.
            Pre-baked response example: ``'stub response'`` or ``{'stub': 'response'}``
            A response-determining function may operate on any arguments
            provided to the client's ``call`` method.
            Example of a response-determining function::

                def stub_response(**kwargs):
                    if kwargs.get('params') and kwargs['params'].get('param_key') == 'param_value':
                        return {'stub response': 'for param_key=param_value'}
                    else:
                        return {'default': 'response'}

        :param ``**kwargs``:
            Arbitrary parameters that can match the intended real endpoint.
            These don't do anything for the stub but streamline the interface.
        """
        self.endpoint_params = kwargs or {}
        self.stub_response = stub_response or "stub for {}".format(self.endpoint_params)
