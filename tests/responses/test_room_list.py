from rentomatic.responses.room_list import RoomListResponse


def test_response_success_is_true():
    assert bool(RoomListResponse()) is True


def test_response_success_default_value_should_be_None():
    assert RoomListResponse().value is None

