import datetime
import uuid
from flask import session
from common.database import Database
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
import json

COLLECTION_NAME = "bootcamp"


class BootcampModel(UserMixin):
    def __init__(self, username, bootcamp_name, user_details={}, long_contests=[], _id=None):
        self.username = username
        self.bootcamp_name = bootcamp_name
        self.user_details = user_details
        self.long_contests = long_contests
        self.id = uuid.uuid4().hex if _id is None else _id

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
            "bootcamp_name": self.bootcamp_name,
            "user_details": self.user_details,
            "long_contests": self.long_contests
        }

    def save_to_mongo(self):
        Database.insert(COLLECTION_NAME, self.json())

    def update_to_mongo(self, new_values):
        json = self.json()
        updated_values = json
        for key in new_values:
            if key in json and key != "username":
                updated_values[key] = new_values[key]
        Database.update_one_set(COLLECTION_NAME, {"username": self.username}, updated_values)
