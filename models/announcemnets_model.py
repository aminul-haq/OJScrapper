import uuid
from common.database import Database
from flask_login import UserMixin

COLLECTION_NAME = "announcements"


class AnnouncementsModel(UserMixin):
    def __init__(self, announcement="", added_on=0, expires_on=0, group="", _id=None):
        self.announcement = announcement
        self.id = uuid.uuid4().hex if _id is None else _id
        self.added_on = added_on
        self.expires_on = expires_on
        self.group = group

    @classmethod
    def get_all_announcements(cls):
        data = Database.get_all_records(COLLECTION_NAME, {})
        return data

    @classmethod
    def get_by_announcement(cls, announcement):
        data = Database.find_one(COLLECTION_NAME, {"announcement": announcement})
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
            "announcement": self.announcement,
            "added_on": self.added_on,
            "expires_on": self.expires_on,
            "group": self.group
        }

    def save_to_mongo(self):
        Database.insert(COLLECTION_NAME, self.json())

    def delete_from_db(self):
        Database.remove(COLLECTION_NAME, {"_id": self.id})

    def update_to_mongo(self, new_values={}):
        json = self.json()
        updated_values = json
        for key in new_values:
            if key in json and key != "_id":
                updated_values[key] = new_values[key]
        Database.update_one_set(COLLECTION_NAME, {"_id": self.id}, updated_values)
