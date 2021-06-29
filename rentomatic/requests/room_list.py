VALID_FILTERS = {
    'code': ['eq', ],
    'price': ['eq', 'lt', 'gt']
}


class RoomListValidRequest:
    def __init__(self, filters):
        self.filters = filters

    @staticmethod
    def has_errors():
        return False


class RoomListInvalidRequest:
    def __init__(self):
        self.errors = []

    def add_error(self, parameter, message):
        self.errors.append({'parameter': parameter,
                            'message': message})

    def __bool__(self):
        return False

    def has_errors(self):
        return bool(self.errors)


def build_room_list_request(filters=None):
    invalid_rq = RoomListInvalidRequest()

    if filters is not None:

        if not isinstance(filters, dict):
            invalid_rq.add_error('filters', 'Is not a dict')
            return invalid_rq

        for key, value in filters.items():
            if isinstance(key, str):
                attr, *op = key.split('__')
                op = op[0] if len(op) == 1 else 'ERROR'
                valid_ops = VALID_FILTERS.get(attr, [])
                if op not in valid_ops:
                    invalid_rq.add_error('filters', f'Invalid filter key: {key}')
            else:
                invalid_rq.add_error('filters', f'Invalid filter key: {key}')

    if invalid_rq.has_errors():
        return invalid_rq
    else:
        return RoomListValidRequest(filters=filters)
