import uuid
from common.database import Database
from flask_login import UserMixin

COLLECTION_NAME = "announcements"


class AnnouncementsModel(UserMixin):
    def __init__(self, name, announcement_list=[], _id=None):
        self.name = name
        self.id = uuid.uuid4().hex if _id is None else _id
        self.announcement_list = announcement_list

    @classmethod
    def get_announcements(cls):
        data = Database.find_one(COLLECTION_NAME, {"name": "announcements"})
        if data is not None:
            return cls(**data)
        else:
            data = AnnouncementsModel(name="announcements")
            data.save_to_mongo()
            return data

    def add_announcement(self, new_announcement):
        self.announcement_list.append(new_announcement)
        self.update_to_mongo()

    def add_announcement_list(self, new_announcement):
        self.announcement_list.extend(new_announcement)
        self.update_to_mongo()

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
            "announcement_list": self.announcement_list
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
