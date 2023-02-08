from bson import ObjectId

import pymongo
from pymongo import MongoClient


class DataBase:
    def __init__(self, db_uri: str, db_name: str) -> None:
        self._client = MongoClient(db_uri)
        self._db = self._client[db_name]

        self.disciplines_collection.create_index(
            [
                ('user_id', pymongo.ASCENDING),
                ('discipline_name', pymongo.ASCENDING)
            ])

    @property
    def disciplines_collection(self):
        return self._db['disciplines']

    def add_discipline(self, discipline_name: str, user_id: int) -> None:
        record = {
            'discipline_name': discipline_name,
            'user_id': user_id
        }
        self.disciplines_collection.insert_one(record)

    def list_disciplines(self, user_id) -> list:
        return list(self.disciplines_collection.find({'user_id': user_id}))

    def add_item_to_discipline(self, user_id: int, discipline_name: str, item_data: dict) -> None:
        collection = self._db[f'{user_id}-{discipline_name}']
        collection.insert_one(item_data)

    def get_discipline_items(self, user_id: int, discipline_name: str) -> list:
        collection = self._db[f'{user_id}-{discipline_name}']
        return list(collection.find())

    def remove_discipline(self, document_id: str) -> None:
        self.disciplines_collection.delete_one({'_id': ObjectId(document_id)})
