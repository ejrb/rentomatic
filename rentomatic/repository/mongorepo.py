from collections import defaultdict

import pymongo

from rentomatic.domain import room


class MongoRepo:
    def __init__(self, config):
        client = pymongo.MongoClient(
            host=config['MONGODB_HOSTNAME'],
            port=int(config['MONGODB_PORT']),
            username=config['MONGODB_USER'],
            password=config['MONGODB_PASSWORD'],
            authSource='admin',
        )
        self.db = client[config['APPLICATION_DB']]

    def list(self, filters=None):
        queries = []
        if filters:
            for key, value in filters.items():
                key, operator = key.split('__')
                queries.append({key: {f'${operator}': value}})

        if len(queries) > 1:
            query = {'$and': queries}
        elif queries:
            query = queries[0]
        else:
            query = {}

        return self._create_room_objects(self.db.rooms.find(query))

    @staticmethod
    def _create_room_objects(rooms):
        return [
            room.Room(
                code=r['code'],
                price=r['price'],
                size=r['size'],
                longitude=r['longitude'],
                latitude=r['latitude']
            )
            for r in rooms
        ]
