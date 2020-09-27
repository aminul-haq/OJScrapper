import threading

from apscheduler.schedulers.background import BackgroundScheduler
from common import solve_updater
from email_service import mail_sender
from models.user_model import UserModel
from models.whitlist_emails_model import WhitelistEmailsModel
from models.announcemnets_model import AnnouncementsModel
from models.todos_model import TodosModel
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


class EmailSender(Resource):
    @jwt_required
    def post(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400

        data = request.get_json()
        if not data or "user_list" not in data or "email_list" not in data:
            return {MESSAGE: "Invalid data"}, 400
        if "subject" not in data or "body" not in data:
            return {MESSAGE: "Invalid data"}, 400

        receivers_list = data["email_list"]
        subject = data["subject"]
        body = data["body"]
        threading.Thread(target=mail_sender.send_mail, args=[receivers_list, subject, body]).start()
        return {MESSAGE: "Mail is being sent"}, 200


class Announcements(Resource):
    @jwt_required
    def get(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400
        announcements = AnnouncementsModel.get_all_announcements()
        if not announcements:
            return {MESSAGE: "no announcements found"}, 400
        else:
            return {"announcements_list": announcements}, 200

    @jwt_required
    def post(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400

        data = request.get_json()
        if "announcements_list" not in data:
            return {MESSAGE: "Invalid data"}, 400

        for announcement in data["announcements_list"]:
            new_announcement = TodosModel(**announcement)
            new_announcement.save_to_mongo()

        return {MESSAGE: "announcements added"}, 200

    @jwt_required
    def delete(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400

        data = request.get_json()
        if "announcements_list" not in data:
            return {MESSAGE: "Invalid data"}, 400

        for announcement in data["announcements_list"]:
            new_announcement = TodosModel(**announcement)
            new_announcement.delete_from_db()

        return {MESSAGE: "announcements removed"}, 200


class Todos(Resource):
    @jwt_required
    def get(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400
        todos = TodosModel.get_all_todos()
        if not todos:
            return {MESSAGE: "no todos found"}, 400
        else:
            return {"todos_list": todos}, 200

    @jwt_required
    def post(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400

        data = request.get_json()
        if "todos_list" not in data:
            return {MESSAGE: "Invalid data"}, 400

        for todo in data["todos_list"]:
            new_todo = TodosModel(**todo)
            new_todo.save_to_mongo()

        return {MESSAGE: "todos added"}, 200

    @jwt_required
    def delete(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400

        data = request.get_json()
        if "todos_list" not in data:
            return {MESSAGE: "Invalid data"}, 400

        for todo in data["todos_list"]:
            new_todo = TodosModel(**data)
            new_todo.delete_from_db()

        return {MESSAGE: "todos removed"}, 200


class WhitelistEmail(Resource):
    @jwt_required
    def get(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400
        whitelist_email = WhitelistEmailsModel.get_whitelisted_email_list()
        return {"email_list": whitelist_email.email_list}, 200

    @jwt_required
    def post(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400

        data = request.get_json()
        if not data or "email_list" not in data:
            return {MESSAGE: "Invalid data"}, 400

        whitelist_email = WhitelistEmailsModel.get_whitelisted_email_list()
        whitelist_email.email_list.extend(data["email_list"])
        whitelist_email.email_list = list(set(whitelist_email.email_list))
        whitelist_email.update_to_mongo()
        return {MESSAGE: "emails added to whitelist"}, 200

    @jwt_required
    def delete(self):
        user = UserModel.get_by_username(get_jwt_identity())
        if not user:
            return {MESSAGE: "user not found"}, 404
        if not user.is_admin:
            return {MESSAGE: "admin privilege required"}, 400

        data = request.get_json()
        if not data or "email_list" not in data:
            return {MESSAGE: "Invalid data"}, 400

        whitelist_email = WhitelistEmailsModel.get_whitelisted_email_list()
        for removed_email in data["email_list"]:
            whitelist_email.email_list.remove(removed_email)

        whitelist_email.update_to_mongo()
        return {MESSAGE: "emails removed from whitelist"}, 200
