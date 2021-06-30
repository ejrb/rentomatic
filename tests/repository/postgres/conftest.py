from contextlib import closing

import pytest
import sqlalchemy

from rentomatic.repository.postgres_objects import Base, Room


@pytest.fixture(scope='session')
def pg_session_empty(app_configuration):
    conn_str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        app_configuration['POSTGRES_USER'],
        app_configuration['POSTGRES_PASSWORD'],
        app_configuration['POSTGRES_HOSTNAME'],
        app_configuration['POSTGRES_PORT'],
        app_configuration['APPLICATION_DB']
    )

    engine = sqlalchemy.create_engine(conn_str)
    connection = engine.connect()

    with closing(connection):
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine

        DBSession = sqlalchemy.orm.sessionmaker(bind=engine)

        session = DBSession()
        with closing(session):
            yield session


@pytest.fixture(scope='session')
def pg_test_data():
    return [
        {
            'code': '49040fcb-74d4-4762-b914-852602347912',
            'size': 205,
            'price': 39,
            'longitude': -0.09998975,
            'latitude': 51.75436293
        },
        {
            'code': 'c95319ef-7b27-47bb-8b1b-5dda3946170d',
            'size': 405,
            'price': 66,
            'longitude': 0.18228006,
            'latitude': 51.74640997
        },
        {
            'code': 'a75e7615-a414-4742-b3fa-e34f0c1854fb',
            'size': 56,
            'price': 60,
            'longitude': 0.27891577,
            'latitude': 51.45994069
        },
        {
            'code': 'd15602fd-d07c-4d8f-9520-5270ec0b31a1',
            'size': 93,
            'price': 48,
            'longitude': 0.33894476,
            'latitude': 51.39916678
        }
    ]


@pytest.fixture(scope='function')
def pg_session(pg_session_empty, pg_test_data):
    for r in pg_test_data:
        new_room = Room(**r)
        pg_session_empty.add(new_room)
        pg_session_empty.commit()

    try:
        yield pg_session_empty
    finally:
        pg_session_empty.query(Room).delete()
