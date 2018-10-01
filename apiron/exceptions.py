class APIException(Exception):
    pass


class NoHostsAvailableException(APIException):
    def __init__(self, service_name):
        message = 'No hosts available for service: {service_name}'.format(service_name=service_name)
        super().__init__(message)


class UnfulfilledParameterException(APIException):
    def __init__(self, endpoint_path, unfulfilled_params):
        message = (
            'The {endpoint_path} endpoint '
            'was called without required parameters: {unfulfilled_params}'.format(
                endpoint_path=endpoint_path,
                unfulfilled_params=unfulfilled_params,
            )
        )
        super().__init__(message)
