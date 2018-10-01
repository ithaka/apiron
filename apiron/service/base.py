class Service:
    """
    A base class for low-level services.

    A service has a domain off of which one or more endpoints stem.
    """

    def get_hosts(self):
        """
        The fully-qualified hostnames that correspond to this service.
        These are often determined by asking a load balancer or service discovery mechanism.

        :return:
            The hostname strings corresponding to this service
        :rtype:
            list
        """
        return [self.domain]

    @property
    def required_headers(self):
        """
        Headers that are required when making calls to this :class:`Service`

        :return:
            Pairs of required header name, header value when calling this service
        :rtype:
            dict
        """
        return {}

    def __str__(self):
        return self.domain

    def __repr__(self):
        return '{klass}(domain={domain})'.format(klass=self.__class__.__name__, domain=self.domain)
