import pytest

from rentomatic.repository import postgresrepo

pytestmark = pytest.mark.integration


def test_repository_list_without_parameters(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_rooms = repo.list()

    assert {
               r.code for r in repo_rooms
           } == {
               r['code'] for r in pg_test_data
           }
