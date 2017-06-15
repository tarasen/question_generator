from bson import ObjectId
from pymongo import MongoClient


class DbAdapter:
    def find(self, **kwargs):
        pass

    def add(self, **kwargs):
        pass

    def update(self, _id, **kwargs):
        pass

    @staticmethod
    def create_mongo(db_name: str, collection: str) -> 'DbAdapter':
        return MongoAdapter(db_name, collection)


class MongoAdapter(DbAdapter):
    def __init__(self, db_name, collection):
        client = MongoClient('mongodb://localhost/' + db_name)
        self.db = client[db_name][collection]

    def find(self, **kwargs):
        return self.db.find(kwargs)

    def add(self, **kwargs):
        self.db.insert(kwargs)

    def update(self, _id, **kwargs):
        self.db.update_one({'_id': ObjectId(_id)}, {"$set": kwargs})
