from rentomatic.responses.room_list import RoomListResponse


def room_list_use_case(repo, request):
    rooms = repo.list()
    return RoomListResponse(rooms)
