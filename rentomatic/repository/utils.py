from operator import eq, lt, gt


class DictFilter:
    OPS = {
        'eq': eq,
        'lt': lt,
        'gt': gt,
    }

    def __init__(self, filters=()):
        self.filters = filters

    @classmethod
    def make_filter_fn(cls, key, value):
        item_key, op_key = key.split('__')
        op = cls.OPS[op_key]
        return lambda item: op(item[item_key], value)

    @classmethod
    def from_queries(cls, query_params: dict):
        filters = [
            cls.make_filter_fn(k, v)
            for k, v in (query_params or {}).items()
        ]

        return cls(filters)

    def apply(self, items):
        return (i for i in items if all(f(i) for f in self.filters))
