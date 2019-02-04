class StubEndpoint:
    """
    A stub endpoint designed to return a pre-baked response

    The intent is to allow for a service to be implemented
    before the endpoint is complete.
    """

    def __init__(self, stub_response=None, **kwargs):
        """
        :param stub_response:
            A pre-baked response, like ``'stub response'`` or ``{'stub': 'response'}``
        :param ``**kwargs``:
            Arbitrary parameters that can match the intended real endpoint.
            These don't do anything for the stub but streamline the interface.
        """
        self.endpoint_params = kwargs if kwargs else {}
        self.stub_response = stub_response or 'stub for {}'.format(self.endpoint_params)
