import uuid
from common.database import Database
from flask_login import UserMixin

COLLECTION_NAME = "todos"


class TodosModel(UserMixin):
    def __init__(self, name, todos_list=[], _id=None):
        self.name = name
        self.id = uuid.uuid4().hex if _id is None else _id
        self.todos_list = todos_list

    @classmethod
    def get_todos(cls):
        data = Database.find_one(COLLECTION_NAME, {"name": "todos"})
        if data is not None:
            return cls(**data)
        else:
            data = TodosModel(name="todos")
            data.save_to_mongo()
            return data

    def add_todo(self, new_todo):
        self.todos_list.append(new_todo)
        self.update_to_mongo()

    def add_todo_list(self, new_todo):
        self.todos_list.extend(new_todo)
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
            "todos_list": self.todos_list
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
