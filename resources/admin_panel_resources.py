import threading

from apscheduler.schedulers.background import BackgroundScheduler
from common import solve_updater
from models.user_model import UserModel
from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)

MESSAGE = "message"


def update_data():
    threading.Thread(target=solve_updater.update_everything()).start()


cron_job = BackgroundScheduler(daemon=True)
cron_job.add_job(update_data, "interval", hours=6, id="update_data")


class DataUpdater(Resource):
    @jwt_required
    def get(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400
        return {
            "interval": str(cron_job.get_job("update_data").trigger),
            "next_run_time": str(cron_job.get_job("update_data").next_run_time)
        }, 200

    @jwt_required
    def post(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400

        data = request.get_json()
        level = data["level"]
        interval = data["interval"]
        if not user or not user.is_admin:
            return {"Message", "admin privilege requires"}, 400
        if level == "days":
            cron_job.reschedule_job(job_id="update_data", trigger="interval", days=interval)
        elif level == "hours":
            cron_job.reschedule_job(job_id="update_data", trigger="interval", hours=interval)
        elif level == "minutes":
            cron_job.reschedule_job(job_id="update_data", trigger="interval", minutes=interval)
        else:
            return {"Message", "invalid data"}, 400
        return {MESSAGE: "data updater rescheduled"}, 200
