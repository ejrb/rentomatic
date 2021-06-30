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
