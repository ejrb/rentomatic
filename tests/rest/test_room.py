import json
from unittest import mock

from rentomatic.domain.room import Room

room_dict = {
    'code': 'a75e7615-a414-4742-b3fa-e34f0c1854fb',
    'size': 56,
    'price': 60,
    'longitude': 0.27891577,
    'latitude': 51.45994069
}
rooms = [
    Room.from_dict(room_dict)
]


@mock.patch('application.rest.room.room_list_use_case')
def test_get(mock_use_case, client):
    mock_use_case.return_value = rooms

    http_response = client.get("/rooms")

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
    mock_use_case.assert_called()
    assert json.loads(http_response.data.decode('utf-8')) == [room_dict]
