import datetime
import threading

from flask_restful import Resource, reqparse
from flask import request
from apscheduler.schedulers.background import BackgroundScheduler
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
from common.solve_updater import update_user_with_username, update_everything

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
        user = UserModel.get_by_username(get_jwt_identity())
        if not user.is_admin:
            return {MESSAGE: "Admin privilege required"}, 401
        # update_everything()
        threading.Thread(target=update_everything).start()
        return {MESSAGE: "Data is being updated"}, 200


class User(Resource):
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
    def post(cls):
        data = request.get_json()
        if data and USERNAME in data:
            user = UserModel.get_by_username(data[USERNAME])
            oj_data = OjModel.get_by_username(data[USERNAME])
            if not user:
                return {MESSAGE: "User Not Found"}, 404
            else:
                return {
                           FIRST_NAME: user.first_name,
                           LAST_NAME: user.last_name,
                           USERNAME: user.username,
                           EMAIL: user.email,
                           OJ_INFO: oj_data.oj_info if oj_data else {},
                           "delete_access": user.is_admin
                       }, 200

        else:
            user_list = []
            for user in UserModel.get_all_users():
                oj_data = OjModel.get_by_username(user[USERNAME])
                user_list.append(
                    {
                        FIRST_NAME: user[FIRST_NAME],
                        LAST_NAME: user[LAST_NAME],
                        USERNAME: user[USERNAME],
                        EMAIL: user[EMAIL],
                        OJ_INFO: oj_data.oj_info if oj_data else {}
                    }
                )
            return {
                       "user_list": user_list,
                       "delete_access": UserModel.get_by_username(get_jwt_identity()).is_admin
                   }, 200

    @jwt_required
    def put(self):
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

        update_user_with_username(user.username)
        return {MESSAGE: "data updated"}, 200

    @jwt_required
    def delete(cls):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400
        data = request.get_json()
        user = UserModel.get_by_username(data[USERNAME])
        if not user:
            return {MESSAGE: "User Not Found"}, 404
        user.delete_from_db()
        oj_info = OjModel.get_by_username(data[USERNAME])
        oj_info.delete_from_db()
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

        update_user_with_username(user.username)
        return {MESSAGE: "data updated"}, 200


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = UserModel.get_by_username(data[USERNAME])
        if user and UserModel.login_valid_username(data[USERNAME], data[PASSWORD]):
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=data[USERNAME], fresh=True, expires_delta=expires)
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
