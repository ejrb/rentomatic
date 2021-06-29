import json

from flask import Blueprint, Response

from rentomatic.repository.memrepo import MemRepo
from rentomatic.serializers.room import RoomJsonEncoder
from rentomatic.use_cases.room_list import room_list_use_case

blueprint = Blueprint('room', __name__)

rooms = [
    {
        'code': '49040fcb-74d4-4762-b914-852602347912',
        'size': 205,
        'price': 39,
        'longitude': -0.09998975,
        'latitude': 51.75436293
    },
    {
        'code': 'c95319ef-7b27-47bb-8b1b-5dda3946170d',
        'size': 405,
        'price': 66,
        'longitude': 0.18228006,
        'latitude': 51.74640997
    },
    {
        'code': 'a75e7615-a414-4742-b3fa-e34f0c1854fb',
        'size': 56,
        'price': 60,
        'longitude': 0.27891577,
        'latitude': 51.45994069
    },
    {
        'code': 'd15602fd-d07c-4d8f-9520-5270ec0b31a1',
        'size': 93,
        'price': 48,
        'longitude': 0.33894476,
        'latitude': 51.39916678
    }
]


@blueprint.route('/rooms', methods=['GET'])
def room_list():
    repo = MemRepo(rooms)
    result = room_list_use_case(repo)
    return Response(
        json.dumps(result, cls=RoomJsonEncoder),
        mimetype='application/json',
        status=200
    )
