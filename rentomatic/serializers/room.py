from json import JSONEncoder
from typing import Any


class RoomJsonEncoder(JSONEncoder):

    def default(self, o: Any) -> Any:
        try:
            return {
                "code": str(o.code),
                "size": o.size,
                "price": o.price,
                "longitude": o.longitude,
                "latitude": o.latitude,
            }
        except AttributeError:
            return super().default(o)
