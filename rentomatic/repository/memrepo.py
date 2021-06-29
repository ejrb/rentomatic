from rentomatic.domain.room import Room


class MemRepo:
    def __init__(self, rooms_data):
        self.rooms_data = rooms_data

    def list(self):
        return [Room.from_dict(r) for r in self.rooms_data]
