import datetime
import uuid
from flask import session
from common.database import Database
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
import json

COLLECTION_NAME = "student"


class StudentModel(UserMixin):
    def __init__(self, username, email,  classroom_name, user_details={}, long_contests=[], _id=None):
        self.username = username
        self.email = email
        self.classroom_name = classroom_name
        self.user_details = user_details
        self.long_contests = long_contests
        self.id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one(COLLECTION_NAME, {"username": username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_username_and_classroom_name(cls, username, classroom_name):
        data = Database.find_one(COLLECTION_NAME, {"username": username, "classroom_name": classroom_name})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(COLLECTION_NAME, {"_id": _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_all_students(cls, query={}):
        return Database.get_all_records(COLLECTION_NAME, query)

    @classmethod
    def remove(self, query):
        return Database.remove(COLLECTION_NAME, query)

    def json(self):
        return {
            "_id": self.id,
            "username": self.username,
            "email": self.email,
            "classroom_name": self.classroom_name,
            "user_details": self.user_details,
            "long_contests": self.long_contests
        }

    def save_to_mongo(self):
        Database.insert(COLLECTION_NAME, self.json())

    def update_to_mongo(self, new_values):
        json = self.json()
        updated_values = json
        for key in new_values:
            if key in json and key != "username" and key != "_id":
                updated_values[key] = new_values[key]
        del updated_values['_id']
        Database.update_one_set(COLLECTION_NAME, {"username": self.username}, updated_values)
