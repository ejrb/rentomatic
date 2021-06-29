from rentomatic.requests.room_list import RoomListInvalidRequest
from rentomatic.responses import (
    ResponseTypes,
    ResponseSuccess,
    ResponseFailure,
    build_response_from_invalid_request
)

SUCCESS_VALUE = {'key': ['value1', 'value2']}
GENERIC_RESPONSE_TYPE = 'Response'
GENERIC_RESPONSE_MESSAGE = 'This is a response'


def test_response_success_is_true():
    response = ResponseSuccess(SUCCESS_VALUE)
    assert bool(response) is True
    assert response.type == ResponseTypes.SUCCESS
    assert response.value == SUCCESS_VALUE


def test_response_failure_is_false():
    response = ResponseFailure(
        GENERIC_RESPONSE_TYPE,
        GENERIC_RESPONSE_MESSAGE
    )

    assert bool(response) is False
    assert response.type == GENERIC_RESPONSE_TYPE
    assert response.message == GENERIC_RESPONSE_MESSAGE


def test_response_failure_init_with_exception():
    response = ResponseFailure(
        GENERIC_RESPONSE_TYPE,
        Exception('Some error message')
    )

    assert bool(response) is False
    assert response.type == GENERIC_RESPONSE_TYPE
    assert response.message == 'Exception: Some error message'


def test_response_failure_from_empty_invalid_request():
    response = build_response_from_invalid_request(
        RoomListInvalidRequest()
    )

    assert bool(response) is False
    assert response.type == ResponseTypes.PARAMETERS_ERROR


def test_response_failure_from_invalid_request_with_errors():
    request = RoomListInvalidRequest()
    request.add_error('path', 'Is mandatory')
    request.add_error('path', "Can't be blank")

    response = build_response_from_invalid_request(request)

    assert bool(response) is False
    assert response.type == ResponseTypes.PARAMETERS_ERROR
    assert response.message == "path: Is mandatory\npath: Can't be blank"
