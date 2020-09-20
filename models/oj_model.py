import uuid
from common.database import Database
from flask_login import UserMixin
from common.OjMap import oj_list

COLLECTION_NAME = "oj_info"


class OjModel(UserMixin):
    def __init__(self, username, oj_info={}, _id=None):
        self.username = username
        self.id = uuid.uuid4().hex if _id is None else _id
        self.oj_info = oj_info

    @classmethod
    def get_vjudge_username(cls, username):
        user = OjModel.get_by_username(username)
        if user and "VJudge" in user.oj_info and "username" in user.oj_info["VJudge"]:
            return user.oj_info["VJudge"]["username"]
        return None

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
            "_id": self.id,
            "username": self.username,
            "oj_info": self.oj_info
        }

    def save_to_mongo(self):
        Database.insert(COLLECTION_NAME, self.json())

    def delete_from_db(self):
        Database.remove(COLLECTION_NAME, {"username": self.username})

    def update_to_mongo(self, new_values):
        json = self.json()
        updated_values = json
        for key in new_values:
            if key in json and key != "username":
                updated_values[key] = new_values[key]
        Database.update_one_set(COLLECTION_NAME, {"username": self.username}, updated_values)
