from flask_restful import Resource, reqparse
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.user_model import UserModel
from models.classroom_model import ClassroomModel
from common.blacklist import BLACKLIST
from models.oj_model import OjModel
from common.solve_updater import update_one, update_all

FIRST_NAME = "first_name"
LAST_NAME = "last_name"
USERNAME = "username"
EMAIL = "email"
MESSAGE = "message"
OJ_INFO = "oj_info"
PASSWORD = "password"


class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        if UserModel.get_by_username(data[USERNAME]):
            return {MESSAGE: "A user with that username already exists"}, 400

        if UserModel.get_by_email(data[EMAIL]):
            return {MESSAGE: "A user with that email already exists"}, 400

        data["password"] = UserModel.encrypt_password(data["password"])
        user = UserModel(**data)
        user.save_to_mongo()

        oj_data = OjModel(data[USERNAME])
        oj_data.save_to_mongo()

        return {MESSAGE: "User created successfully."}, 201


class OJUpdate(Resource):
    @jwt_required
    def post(self):
        claims = get_raw_jwt()
        print(claims)
        if claims["identity"] != "admin":
            return {MESSAGE: "Admin privilege required"}, 401
        update_all()


class Classroom(Resource):
    @jwt_required
    def get(self):
        data = request.get_json()
        if "classroom_name" in data:
            classroom = ClassroomModel.get_by_classroom_name(data["classroom_name"])
            if classroom:
                return ClassroomModel.get_by_classroom_name(data["classroom_name"]).json(), 200
        return {MESSAGE: "Classroom Not Found"}, 200

    @jwt_required
    def post(self):
        data = request.get_json()
        classroom = ClassroomModel(**data)
        classroom.save_to_mongo()
        return {MESSAGE: "Classroom created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, username: str):
        user = UserModel.get_by_username(username)
        if not user:
            return {MESSAGE: "User Not Found"}, 404
        return user.json(), 200

    @classmethod
    @jwt_required
    def delete(cls, username: str):
        claims = get_raw_jwt()
        if not claims["identity"] == "admin":
            return {MESSAGE: "Admin privilege required"}, 401
        user = UserModel.get_by_username(username)
        if not user:
            return {MESSAGE: "User Not Found"}, 404
        user.delete_from_db()
        return {MESSAGE: "User deleted."}, 200


class Lookup(Resource):
    @jwt_required
    def get(self):
        data = request.get_json()
        if data and USERNAME in data and EMAIL in data:
            user_by_username = UserModel.get_by_username(data[USERNAME])
            user_by_email = UserModel.get_by_username(data[EMAIL])
            res = {
                "username_exist": user_by_username is not None,
                "email_exist": user_by_email is not None
            }
            return res, 200
        return {MESSAGE: "bad request"}, 400


class UserInfo(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        user = UserModel.get_by_username(identity)
        if not user:
            return {MESSAGE: "user not found"}, 400
        oj_data = OjModel.get_by_username(identity)
        return {
                   FIRST_NAME: user.first_name,
                   LAST_NAME: user.last_name,
                   USERNAME: user.username,
                   EMAIL: user.email,
                   OJ_INFO: oj_data.oj_info if oj_data else {}
               }, 200

    @jwt_required
    def post(self):
        data = request.get_json()
        identity = get_jwt_identity()
        user = UserModel.get_by_username(identity)

        if not user:
            return {MESSAGE: "user not found"}, 400

        if EMAIL in data:
            email_user = UserModel.get_by_email(data[EMAIL])
            if EMAIL in data and email_user and email_user != user:
                return {MESSAGE: "email already exists"}, 400

        user.update_to_mongo(data)

        oj_info = OjModel.get_by_username(identity)
        if oj_info:
            oj_info.update_to_mongo(data)

        update_one(user.username)
        return {MESSAGE: "data updated"}, 200


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = UserModel.get_by_username(data[USERNAME])
        if user and UserModel.login_valid_username(data[USERNAME], data[PASSWORD]):
            access_token = create_access_token(identity=data[USERNAME], fresh=True)
            refresh_token = create_refresh_token(data[USERNAME])
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200

        return {MESSAGE: "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {MESSAGE: "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        Get a new access token without requiring username and password—only the "refresh token"
        provided in the /login endpoint.

        Note that refreshed access tokens have a `fresh=False`, which means that the user may have not
        given us their username and password for potentially a long time (if the token has been
        refreshed many times over).
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
