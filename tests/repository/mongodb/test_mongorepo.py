import pytest

from rentomatic.repository import mongorepo

pytestmark = pytest.mark.integration


@pytest.fixture
def repo(app_configuration):
    return mongorepo.MongoRepo(app_configuration)


def test_repository_list_without_parameters(
    repo, mg_database, mg_test_data
):
    repo_rooms = repo.list()

    assert {
               r.code for r in repo_rooms
           } == {
               r['code'] for r in mg_test_data
           }


def test_repository_list_with_code_equal_filter(
    repo, mg_database, mg_test_data
):
    code = mg_test_data[0]['code']
    repo_rooms = repo.list(
        filters={'code__eq': code}
    )

    assert len(repo_rooms) == 1
    assert repo_rooms[0].code == code


def test_repository_list_with_price_equal_filter(
    repo, mg_database, mg_test_data
):
    repo_rooms = repo.list(
        filters={'price__eq': 60}
    )

    assert len(repo_rooms) == 1
    assert repo_rooms[0].price == 60
    assert repo_rooms[0].code == 'a75e7615-a414-4742-b3fa-e34f0c1854fb'


def test_repository_list_with_price_greater_than_filter(
    repo, mg_database, mg_test_data
):
    repo_rooms = repo.list(
        filters={'price__gt': 60}
    )

    assert len(repo_rooms) == 1
    assert repo_rooms[0].price > 60
    assert repo_rooms[0].code == 'c95319ef-7b27-47bb-8b1b-5dda3946170d'


def test_repository_list_with_price_less_than_filter(
    repo, mg_database, mg_test_data
):
    repo_rooms = repo.list(
        filters={'price__lt': 40}
    )

    assert len(repo_rooms) == 1
    assert repo_rooms[0].price < 40
    assert repo_rooms[0].code == '49040fcb-74d4-4762-b914-852602347912'


def test_repository_list_with_price_between_filter(
    repo, mg_database, mg_test_data
):
    repo_rooms = repo.list(
        filters={'price__gt': 40, 'price__lt': 50}
    )

    assert len(repo_rooms) == 1
    assert 40 < repo_rooms[0].price < 50
    assert repo_rooms[0].code == 'd15602fd-d07c-4d8f-9520-5270ec0b31a1'
