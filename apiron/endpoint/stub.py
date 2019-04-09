class StubEndpoint:
    """
    A stub endpoint designed to return a pre-baked response

    The intent is to allow for a service to be implemented
    before the endpoint is complete.
    """
    def __call__(self, **kwargs):
        return self.stub_response(**kwargs) if callable(self.stub_response) else self.stub_response

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
        self.stub_response = stub_response or 'stub for {}'.format(self.endpoint_params)
