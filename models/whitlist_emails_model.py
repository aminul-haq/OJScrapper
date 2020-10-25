import uuid
from common.database import Database
from flask_login import UserMixin

COLLECTION_NAME = "whitelist_email"


class WhitelistEmailsModel(UserMixin):
    def __init__(self, name, email_list=[], _id=None):
        self.name = name
        self.id = uuid.uuid4().hex if _id is None else _id
        self.email_list = email_list

    @classmethod
    def get_whitelisted_email_list(cls):
        data = Database.find_one(COLLECTION_NAME, {"name": "whitelisted_email_list"})
        if data is not None:
            return cls(**data)

    @classmethod
    def check_email(cls, email):
        data = Database.find_one(COLLECTION_NAME, {"name": "whitelisted_email_list"})
        if not data or email in data["email_list"]:
            return True
        return False

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
            "email_list": self.email_list
        }

    def save_to_mongo(self):
        Database.insert(COLLECTION_NAME, self.json())

    def delete_from_db(self):
        Database.remove(COLLECTION_NAME, {"name": self.name})

    def update_to_mongo(self, new_values={}):
        json = self.json()
        updated_values = json
        for key in new_values:
            if key in json and key != "name":
                updated_values[key] = new_values[key]
        Database.update_one_set(COLLECTION_NAME, {"name": self.name}, updated_values)
