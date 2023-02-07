import pymongo
from pymongo import MongoClient


class DataBase:
    def __init__(self, db_uri: str, db_name: str) -> None:
        self._client = MongoClient(db_uri, username='username', password='password')
        self._db = self._client[db_name]

        self._disciplines_collection = self._db['disciplines']

        self.disciplines_collection.create_index(
            [
                ('user_id', pymongo.ASCENDING),
                ('discipline_name', pymongo.ASCENDING)
            ])

    @property
    def disciplines_collection(self):
        return self._disciplines_collection

    def add_discipline(self, discipline_name: str, user_id: int) -> None:
        record = {
            'discipline_name': discipline_name,
            'user_id': user_id
        }
        self.disciplines_collection.insert_one(record)

    def list_disciplines(self, user_id):
        return list(self.disciplines_collection.find({'user_id': user_id}))
