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
import threading

from models.classroom_model import ClassroomModel
from models.user_model import UserModel
from models.student_model import StudentModel
from common import solve_updater

MESSAGE = "message"
CLASSROOM_NAME = "classroom_name"


def update_students(classroom):
    StudentModel.remove({CLASSROOM_NAME: classroom.classroom_name})
    for username in classroom.user_list:
        StudentModel(username, classroom.classroom_name).save_to_mongo()
    solve_updater.update_students(classroom)


class CreateClassroom(Resource):
    @jwt_required
    def post(self):
        user = UserModel.get_by_username(get_jwt_identity())
        data = request.get_json()
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400
        if not data or CLASSROOM_NAME not in data:
            return {MESSAGE: "invalid data"}, 400
        if ClassroomModel.get_by_classroom_name(data[CLASSROOM_NAME]):
            return {MESSAGE: "A classroom with that name already exists"}, 400
        classroom = ClassroomModel(**data)
        for username in classroom.user_list:
            if not UserModel.get_by_username(username):
                return {MESSAGE: "user not found"}, 404
        classroom.save_to_mongo()
        threading.Thread(target=update_students, args=[classroom]).start()
        return {MESSAGE: "Classroom created successfully."}, 201


class Classroom(Resource):
    @jwt_required
    def get(self):
        user = UserModel.get_by_username(get_jwt_identity())
        data = request.get_json()
        if not data or data == {}:
            classroom_list = ClassroomModel.get_all_classrooms()
            return {
                       "classroom_list": classroom_list,
                       "edit_access": user.is_admin
                   }, 200
        elif CLASSROOM_NAME in data:
            classroom = ClassroomModel.get_by_classroom_name(data[CLASSROOM_NAME])
            if classroom:
                return classroom.json(), 200
            else:
                return {MESSAGE: "classroom not found"}, 404
        else:
            return {MESSAGE: "invalid data"}, 400

    @jwt_required
    def post(self):
        user = UserModel.get_by_username(get_jwt_identity())
        data = request.get_json()
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400

        if not data or CLASSROOM_NAME not in data:
            return {MESSAGE: "invalid data"}, 400

        classroom = ClassroomModel.get_by_classroom_name(data[CLASSROOM_NAME])
        if not classroom:
            return {MESSAGE: "classroom not found"}, 404

        for username in data["user_list"]:
            if not UserModel.get_by_username(username):
                return {MESSAGE: "user not found"}, 404

        classroom.update_to_mongo(data)
        classroom = ClassroomModel.get_by_classroom_name(data[CLASSROOM_NAME])
        threading.Thread(target=update_students, args=[classroom]).start()
        return {MESSAGE: "data updated"}, 200

    @jwt_required
    def delete(self):
        user = UserModel.get_by_username(get_jwt_identity())
        data = request.get_json()
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400

        if not ClassroomModel.remove({CLASSROOM_NAME: data[CLASSROOM_NAME]}):
            return {MESSAGE: "invalid data"}, 400
        else:
            StudentModel.remove({CLASSROOM_NAME: data[CLASSROOM_NAME]})
            return {MESSAGE: "classroom deleted"}, 200
