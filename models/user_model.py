from datetime import datetime
import uuid
from flask import session
from common.database import Database
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
import json

COLLECTION_NAME = "users"


class UserModel(UserMixin):
    def __init__(self, email, password, username, first_name="", last_name="", reset_pass={}, _id=None, is_admin=False,
                 classroom_name=None):
        self.email = email
        self.password = password
        self.username = username
        self.id = uuid.uuid4().hex if _id is None else _id
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.reset_pass = reset_pass
        self.classroom_name = classroom_name

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(COLLECTION_NAME, {"email": email})
        if data is not None:
            return cls(**data)

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

    @classmethod
    def get_all_users(cls, query={}):
        return Database.get_all_records(COLLECTION_NAME, query)

    @staticmethod
    def login_valid_email(email, password):
        # Check whether a user's email matches the password they sent us
        user = UserModel.get_by_email(email)
        if user is not None:
            # Check the password
            return check_password_hash(user.password, password)
        return False

    @staticmethod
    def login_valid_username(username, password):
        # Check whether a user's email matches the password they sent us
        user = UserModel.get_by_username(username)
        if user is not None:
            # Check the password
            if not check_password_hash(user.password, password):
                if "expires_on" in user.reset_pass and "temp_pass" in user.reset_pass:
                    if datetime.now().timestamp() <= user.reset_pass["expires_on"]:
                        return check_password_hash(user.reset_pass["temp_pass"], password)
            else:
                return True

        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            # User doesn't exist, so we can create it
            new_user = cls(email, password, "testusername")
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User exists :(
            return False

    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def json(self):
        return {
            "_id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "reset_pass": self.reset_pass,
            "is_admin": self.is_admin,
            "classroom_name": self.classroom_name
        }

    @staticmethod
    def encrypt_password(password):
        return generate_password_hash(password).decode("utf-8")

    def save_to_mongo(self):
        Database.insert(COLLECTION_NAME, self.json())

    # def update_to_mongo(self, new_values):
    #     Database.update_one(COLLECTION_NAME, {"username": self.username}, new_values)

    def update_to_mongo(self, new_values={}):
        json = self.json()
        updated_values = json
        for key in new_values:
            if key in json and key != "username" and key != "is_admin":
                if key == "password":
                    updated_values[key] = generate_password_hash(new_values[key]).decode("utf-8")
                else:
                    updated_values[key] = new_values[key]
        Database.update_one_set(COLLECTION_NAME, {"username": self.username}, updated_values)

    def delete_from_db(self):
        Database.remove(COLLECTION_NAME, {"username": self.username})
