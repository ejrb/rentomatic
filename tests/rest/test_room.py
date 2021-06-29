import json
from unittest import mock

from rentomatic.domain.room import Room
from rentomatic.responses import ResponseSuccess, ResponseFailure, ResponseTypes

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
    mock_use_case.return_value = ResponseSuccess(rooms)

    http_response = client.get("/rooms")

    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args
    assert args[1].filters == {}

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
    assert json.loads(http_response.data.decode('utf-8')) == [room_dict]


@mock.patch('application.rest.room.room_list_use_case')
def test_get_with_filters(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(rooms)

    http_response = client.get("/rooms?filter_price__gt=2&filter_price__lt=6")

    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args
    assert args[1].filters == {
        'price__gt': 2,
        'price__lt': 6
    }

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
    assert json.loads(http_response.data.decode('utf-8')) == [room_dict]


@mock.patch('application.rest.room.room_list_use_case')
def test_get_with_use_case_exception(mock_use_case, client):
    mock_use_case.return_value = ResponseFailure(ResponseTypes.SYSTEM_ERROR,
                                                 'Exception: Oops!')
    http_response = client.get("/rooms")
    mock_use_case.assert_called()
    assert http_response.status_code == 500


@mock.patch('application.rest.room.room_list_use_case')
def test_get_with_invalid_filters(mock_use_case, client):
    mock_use_case.return_value = ResponseFailure(ResponseTypes.PARAMETERS_ERROR,
                                                 'filters: invalid value for code abc')

    http_response = client.get("/rooms?filter_code__gt=abc")

    mock_use_case.assert_called()

    assert http_response.status_code == 400
