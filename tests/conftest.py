import pytest


from application.app import create_app


@pytest.fixture
def app():
    return create_app('test')
