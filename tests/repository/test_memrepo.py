import pytest

from rentomatic.domain.room import Room
from rentomatic.repository.memrepo import MemRepo


@pytest.fixture
def room_dicts():
    return [{'code': '49040fcb-74d4-4762-b914-852602347912', 'size': 205, 'price': 39, 'longitude': -0.09998975, 'latitude': 51.75436293}, {'code': 'c95319ef-7b27-47bb-8b1b-5dda3946170d', 'size': 405, 'price': 66, 'longitude': 0.18228006, 'latitude': 51.74640997}, {'code': 'a75e7615-a414-4742-b3fa-e34f0c1854fb', 'size': 56, 'price': 60, 'longitude': 0.27891577, 'latitude': 51.45994069}, {'code': 'd15602fd-d07c-4d8f-9520-5270ec0b31a1', 'size': 93, 'price': 48, 'longitude': 0.33894476, 'latitude': 51.39916678}]


def test_repository_list_without_parameters(room_dicts):
    repo = MemRepo(room_dicts)

    rooms = [Room.from_dict(r) for r in room_dicts]

    assert repo.list() == rooms
