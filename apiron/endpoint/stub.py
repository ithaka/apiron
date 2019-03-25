class StubEndpoint:
    """
    A stub endpoint designed to return a pre-baked response

    The intent is to allow for a service to be implemented
    before the endpoint is complete.
    """

    def __init__(self, stub_response=None, **kwargs):
        """
        :param stub_response:
            A pre-baked response or response-determining function.
            Pre-baked response example: ``'stub response'`` or ``{'stub': 'response'}``
            A response-determining function may operate on any arguments
            provided to the client's ``call`` method.
            Example of a response-determining function::

                def stub_response(**kwargs):
                    response_map = {
                        'param_value': {'stub response': 'for param_key=param_value'},
                        'default': {'default': 'response'},
                    }
                    data_key = kwargs['params'].setdefault('param_key', 'default')
                    return response_map[data_key]

        :param ``**kwargs``:
            Arbitrary parameters that can match the intended real endpoint.
            These don't do anything for the stub but streamline the interface.
        """
        self.endpoint_params = kwargs if kwargs else {}
        self.stub_response = stub_response or 'stub for {}'.format(self.endpoint_params)
