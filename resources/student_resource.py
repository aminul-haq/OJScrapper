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

from models.classroom_model import ClassroomModel
from models.user_model import UserModel
from models.student_model import StudentModel

MESSAGE = "message"
CLASSROOM_NAME = "classroom_name"
USERNAME = "username"


class Student(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        student = StudentModel.get_all_students(data)
        if not student:
            return {MESSAGE: "Student Not Found"}, 404
        return student, 200

    @jwt_required
    def put(self):
        user = UserModel.get_by_username(get_jwt_identity())
        data = request.get_json()
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400
        if not data or CLASSROOM_NAME not in data:
            return {MESSAGE: "invalid data"}, 400
        student = StudentModel.get_by_username_and_classroom_name(data[USERNAME], data[CLASSROOM_NAME])
        if not student:
            return {MESSAGE: "student not found"}, 404
        student.update_to_mongo(data)
        return {MESSAGE: "data updated"}, 200
