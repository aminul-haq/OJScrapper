import uuid
from common.database import Database
from flask_login import UserMixin

COLLECTION_NAME = "contest_data"


class ContestDataModel(UserMixin):
    def __init__(self, name, updated_on=0, data=[], _id=None):
        self.name = name
        self.id = uuid.uuid4().hex if _id is None else _id
        self.updated_on = updated_on
        self.data = data

    @classmethod
    def get_vjudge_contest_data(cls):
        data = Database.find_one(COLLECTION_NAME, {"name": "vjudge_contest_data"})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_name(cls, name):
        data = Database.find_one(COLLECTION_NAME, {"name": name})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(COLLECTION_NAME, {"_id": _id})
        if data is not None:
            return cls(**data)

    def json(self):
        return {
            "_id": self.id,
            "name": self.name,
            "updated_on": self.updated_on,
            "data": self.data
        }

    def save_to_mongo(self):
        Database.insert(COLLECTION_NAME, self.json())

    def delete_from_db(self):
        Database.remove(COLLECTION_NAME, {"name": self.name})

    def update_to_mongo(self, new_values):
        json = self.json()
        updated_values = json
        for key in new_values:
            if key in json and key != "name":
                updated_values[key] = new_values[key]
        Database.update_one_set(COLLECTION_NAME, {"name": self.name}, updated_values)
