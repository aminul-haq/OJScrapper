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
from models.usermodel import UserModel
from common.blacklist import BLACKLIST


# _user_parser = reqparse.RequestParser()
# _user_parser.add_argument('email',
#                           type=str,
#                           required=False,
#                           help="This field cannot be blank."
#                           )
#
# _user_parser.add_argument('password',
#                           type=str,
#                           required=True,
#                           help="This field cannot be blank."
#                           )
# _user_parser.add_argument('username',
#                           type=str,
#                           required=True,
#                           help="This field cannot be blank."
#                           )


class UserRegister(Resource):
    def post(self):
        data = request.get_json()

        if UserModel.get_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        if UserModel.get_by_username(data['email']):
            return {"message": "A user with that email already exists"}, 400

        user = UserModel(**data)
        user.save_to_mongo()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, username: str):
        user = UserModel.get_by_username(username)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.json(), 200

    @classmethod
    @jwt_required
    def delete(cls, username: str):
        claims = get_raw_jwt()
        if not claims["is_admin"]:
            return {"message": "Admin privilege required"}, 401
        user = UserModel.get_by_username(username)
        if not user:
            return {'message': 'User Not Found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200


class Lookup(Resource):
    @staticmethod
    def get():
        data = request.get_json()
        if data and "username" in data and "email" in data:
            user_by_username = UserModel.get_by_username(data["username"])
            user_by_email = UserModel.get_by_username(data["email"])
            res = {
                "username_exist": user_by_username is not None,
                "email_exist": user_by_email is not None
            }
            return res, 200
        return {"message": "bad request"}, 400


class UserLogin(Resource):
    @staticmethod
    def post(self):
        data = request.get_json()
        user = UserModel.get_by_username(data['username'])
        if user and UserModel.login_valid_username(data["username"], data["password"]):
            access_token = create_access_token(identity=data.username, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        Get a new access token without requiring username and password—only the 'refresh token'
        provided in the /login endpoint.

        Note that refreshed access tokens have a `fresh=False`, which means that the user may have not
        given us their username and password for potentially a long time (if the token has been
        refreshed many times over).
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
