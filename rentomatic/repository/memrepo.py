from rentomatic.domain.room import Room

from rentomatic.repository.utils import DictFilter


class MemRepo:
    def __init__(self, rooms_data):
        self.rooms_data = rooms_data

    def list(self, filters=None):
        filterer = DictFilter.from_queries(filters)
        rooms = filterer.apply(self.rooms_data)

        return [
            Room.from_dict(r)
            for r in
            rooms
        ]
