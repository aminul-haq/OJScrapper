import uuid
from common.database import Database
from flask_login import UserMixin
from common.OjMap import oj_list

COLLECTION_NAME = "classroom"


class ClassroomModel(UserMixin):
    def __init__(self, name, user_list={}, _id=None, is_rated=False, is_bootcamp=False):
        self.name = name
        self.id = uuid.uuid4().hex if _id is None else _id
        self.user_list = user_list
        self.is_rated = is_rated
        self.is_bootcamp = is_bootcamp

    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one(COLLECTION_NAME, {"username": username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(COLLECTION_NAME, {"_id": _id})
        if data is not None:
            return cls(**data)

    def json(self):
        return {
            "username": self.username,
            "user_list": self.oj_info,
            "is_rated": self.is_rated,
            "is_bootcamp": self.is_bootcamp
        }

    def save_to_mongo(self):
        Database.insert(COLLECTION_NAME, self.json())

    def update_to_mongo(self, new_values):
        json = self.json()
        updated_values = json
        for key in new_values:
            if key in json and key != "username":
                updated_values[key] = new_values[key]
        print(updated_values)
        Database.update_one_set(COLLECTION_NAME, {"username": self.username}, updated_values)
