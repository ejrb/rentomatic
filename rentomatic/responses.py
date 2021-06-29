class ResponseTypes:
    SUCCESS = 'success'
    SYSTEM_ERROR = 'system_error'
    PARAMETERS_ERROR = 'parameters_error'


class ResponseFailure:
    def __init__(self, type_, message):
        self.type = type_
        self.message = self._format_message(message)

    @staticmethod
    def _format_message(message):
        if isinstance(message, Exception):
            return f'{message.__class__.__name__}: {message}'
        else:
            return str(message)

    def __bool__(self):
        return False

    @property
    def value(self):
        return {'type': self.type, 'message': self.message}


class ResponseSuccess:
    type = ResponseTypes.SUCCESS

    def __init__(self, value=None):
        self.value = value


def build_response_from_invalid_request(request):
    rt = ResponseTypes.PARAMETERS_ERROR

    message = '\n'.join(
        f"{error['parameter']}: {error['message']}"
        for error in request.errors
    )

    return ResponseFailure(rt, message)
