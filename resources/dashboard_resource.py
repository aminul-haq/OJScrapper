from datetime import datetime, timedelta

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
from models.student_model import StudentModel
from models.contest_data_model import ContestDataModel
from common.blacklist import BLACKLIST
from models.oj_model import OjModel
from common import solve_updater
from common.database import Database
from common.OjMap import *

FIRST_NAME = "first_name"
LAST_NAME = "last_name"
USERNAME = "username"
EMAIL = "email"
MESSAGE = "message"
OJ_INFO = "oj_info"
PASSWORD = "password"


def get_solve_in_time_range(submission_data, username, start, end):
    cnt = 0
    for contest_id in submission_data:
        if username not in submission_data[contest_id]["submission"]:
            continue
        cnt = cnt + solve_updater.count_in_range(submission_data[contest_id]["submission"][username], start, end)
    return cnt


def get_last_day_solve(submission_data, username):
    d = datetime.today() - timedelta(days=1)
    start = int(d.timestamp() * 1000) + 1
    end = int(datetime.today().timestamp() * 1000)
    return get_solve_in_time_range(submission_data, username, start, end)


def get_todos(username):
    user = UserModel.get_by_username(username)
    oj_info = OjModel.get_by_username(username)
    if not user or not oj_info:
        return None
    oj_info = oj_info.oj_info
    todo_list = []
    if VJUDGE not in oj_info or USERNAME not in oj_info[VJUDGE] or not oj_info[VJUDGE][USERNAME]:
        todo_list.append("Please add your Vjudge username in your profile")
    if CODEFORCES not in oj_info or USERNAME not in oj_info[CODEFORCES] or not oj_info[CODEFORCES][USERNAME]:
        todo_list.append("Please add your Codeforces username in your profile")
    if ATCODER not in oj_info or USERNAME not in oj_info[ATCODER] or not oj_info[ATCODER][USERNAME]:
        todo_list.append("Please add your Atcoder username in your profile")

    return todo_list


def get_announcements(username):
    announcement_list = [
        "Please complete your remaining tasks within 28 Sept, 2020"
        "Last Individual contest is due on 25 Sept, 2020 at 2.30 pm",
        "Tentative date for final graduation contest is 16 Oct, 2020"
    ]
    return announcement_list


def get_last_30_days_solve(submission_data, username):
    label = []
    solves = []
    i = 0
    while i < 30:
        d = datetime.today() - timedelta(days=i)
        end = int(d.timestamp() * 1000) + 1
        cnt = get_solve_in_time_range(submission_data, username, 0, end)
        label.append(str(d.strftime("%b %d")))
        solves.append(cnt)
        i = i + 1
    return [label, solves]


class Dashboard(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        username = get_jwt_identity()
        if data and USERNAME in data:
            username = data[USERNAME]
        classroom_name = ""
        if "classroom_name" in data:
            classroom_name = data["classroom_name"]
        else:
            classroom_list = ClassroomModel.get_all_classrooms({})
            # print(username, classroom_list)
            for classroom in classroom_list:
                if username not in classroom["user_list"]:
                    continue
                curr_name = classroom["classroom_name"]
                if curr_name == "rated":
                    classroom_name = curr_name
                    break
                else:
                    if classroom_name == "":
                        classroom_name = curr_name
                    else:
                        if int(curr_name[1, len(curr_name) - 1]) > int(classroom_name[1, len(classroom_name) - 1]):
                            classroom_name = curr_name
        student = StudentModel.get_by_username_and_classroom_name(username, classroom_name)
        if not student:
            return {MESSAGE: "no data found"}, 404

        res = student.json()

        vjudge_username = OjModel.get_vjudge_username(username)
        if not vjudge_username:
            return res, 200

        contest_data = ContestDataModel.get_vjudge_contest_data()
        last_day_solve = get_last_day_solve(contest_data.data, vjudge_username)
        last_30_days_solve = get_last_30_days_solve(contest_data.data, vjudge_username)
        todo_list = get_todos(username)
        announcement_list = get_announcements(username)

        res["last_day_solve"] = last_day_solve
        res["last_30_days_solve"] = last_30_days_solve
        res["todo_list"] = todo_list
        res["announcement_list"] = announcement_list
        return res, 200


class ContestData(Resource):
    @jwt_required
    def get(self):
        contest_data = ContestDataModel.get_vjudge_contest_data()
        return {
                   "name": contest_data.name,
                   "updated_on": contest_data.updated_on,
                   "data": contest_data.data
               }, 200
