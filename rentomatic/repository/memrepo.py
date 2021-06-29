from rentomatic.domain.room import Room

from operator import eq, gt, lt

OPS = {
    'eq': eq,
    'lt': lt,
    'gt': gt,
}


def make_filter_fn(key, op, value):
    return lambda room: OPS[op](room[key], value)


class MemRepo:
    def __init__(self, rooms_data):
        self.rooms_data = rooms_data

    def list(self, filters=None):
        filter_fns = []
        if filters:
            filter_fns = [
                make_filter_fn(*key.split('__'), value)
                for key, value in filters.items()
            ]

        return [
            Room.from_dict(r)
            for r in
            self.rooms_data
            if all(ff(r) for ff in filter_fns)
        ]
