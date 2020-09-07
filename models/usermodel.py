import datetime
import uuid
from flask import session
from common.database import Database
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash


class UserModel(UserMixin):
    def __init__(self, email, password, username, _id=None, is_admin=False):
        self.email = email
        self.password = password
        self.username = username
        self.id = uuid.uuid4().hex if _id is None else _id
        self.is_admin = is_admin

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one("users", {"username": username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

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
            return check_password_hash(user.password, password)
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

    # def get_blogs(self):
    #     return Blog.find_by_author_id(self._id)
    #
    # def new_blog(self, title, description):
    #     blog = Blog(author=self.email,
    #                 title=title,
    #                 description=description,
    #                 author_id=self._id)
    #
    #     blog.save_to_mongo()
    #
    # @staticmethod
    # def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
    #     blog = Blog.from_mongo(blog_id)
    #     blog.new_post(title=title,
    #                   content=content,
    #                   date=date)

    def json(self):
        return {
            "email": self.email,
            "_id": self.id,
            "username": self.username,
            "password": generate_password_hash(self.password).decode("utf-8"),
            "is_admin": self.is_admin
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())
