VALID_FILTERS = {
    'code': (str, ['eq', ]),
    'price': (int, ['eq', 'lt', 'gt'])
}


class RoomListValidRequest:
    def __init__(self, filters=None):
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
    valid_filters = None

    if filters is not None:
        valid_filters = {}

        if not isinstance(filters, dict):
            invalid_rq.add_error('filters', 'Is not a dict')
            return invalid_rq

        for key, value in filters.items():
            if isinstance(key, str):
                attr, *op = key.split('__')
                op = op[0] if len(op) == 1 else 'ERROR'
                type_, valid_ops = VALID_FILTERS.get(attr, (str, []))

                if op not in valid_ops:
                    invalid_rq.add_error('filters', f'Invalid filter key: {key}')

                try:
                    valid_value = type_(value)
                except (TypeError, ValueError):
                    invalid_rq.add_error('filters', f'Invalid filter value for {key}: {value}')
                else:
                    valid_filters[key] = valid_value
            else:
                invalid_rq.add_error('filters', f'Invalid filter key: {key}')

    if invalid_rq.has_errors():
        return invalid_rq
    else:
        return RoomListValidRequest(filters=valid_filters)
