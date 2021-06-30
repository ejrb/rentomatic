from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from rentomatic.domain import room
from rentomatic.repository.postgres_objects import Base, Room


class PostgresRepo:

    def __init__(self, configuration):
        connection_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            configuration["POSTGRES_USER"],
            configuration["POSTGRES_PASSWORD"],
            configuration["POSTGRES_HOSTNAME"],
            configuration["POSTGRES_PORT"],
            configuration["APPLICATION_DB"],
        )
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine

    def list(self):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        query = session.query(Room)

        return self._create_room_objects(query.all())

    @staticmethod
    def _create_room_objects(rooms):
        return [
            room.Room(
                code=r.code,
                price=r.price,
                size=r.size,
                longitude=r.longitude,
                latitude=r.latitude
            )
            for r in rooms
        ]
