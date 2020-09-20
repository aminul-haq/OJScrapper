import datetime

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
from common.solve_updater import update_user_with_username, update_all

FIRST_NAME = "first_name"
LAST_NAME = "last_name"
USERNAME = "username"
EMAIL = "email"
MESSAGE = "message"
OJ_INFO = "oj_info"
PASSWORD = "password"


class Dashboard(Resource):
    @jwt_required
    def post(self):
        return {MESSAGE: "hello"}, 200
