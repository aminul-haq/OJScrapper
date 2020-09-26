import uuid
from common.database import Database
from flask_login import UserMixin
from common.OjMap import oj_list

COLLECTION_NAME = "mail_templates"


class MailTemplate(UserMixin):
    def __init__(self, topic, template_name, subject="", message="", _id=None):
        self.topic = topic
        self.template_name = template_name
        self.id = uuid.uuid4().hex if _id is None else _id
        self.subject = subject
        self.message = message

    @classmethod
    def get_by_template_name(cls, template_name):
        data = Database.find_one(COLLECTION_NAME, {"template_name": template_name})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(COLLECTION_NAME, {"_id": _id})
        if data is not None:
            return cls(**data)

    def json(self):
        return {
            "_id": self.id,
            "topic": self.topic,
            "template_name": self.template_name,
            "subject": self.subject,
            "message": self.message
        }

    def save_to_mongo(self):
        Database.insert(COLLECTION_NAME, self.json())

    def delete_from_db(self):
        Database.remove(COLLECTION_NAME, {"template_name": self.template_name})

    def update_to_mongo(self, new_values={}):
        json = self.json()
        updated_values = json
        for key in new_values:
            if key in json:
                updated_values[key] = new_values[key]
        Database.update_one_set(COLLECTION_NAME, {"template_name": self.template_name}, updated_values)


if __name__ == '__main__':
    Database.initialize()

    print(MailTemplate.get_by_template_name("invitation").message)

    # mail_templates = [
    #     {
    #         "topic": "Invitation",
    #         "template_name": "invitation",
    #         "subject": "Welcome to PScamp!",
    #         "message": "Hello user,\nWe invite you to open an account on https://pscamp.netlify.com/.\n"
    #     },
    #     {
    #         "topic": "Password Reset",
    #         "template_name": "password_reset",
    #         "subject": "Reset Password",
    #         "message": "Hello user,\nYou can use the temporary password below to login to your PScamp account within the next 60 minutes. If you have forgotten your current password, you are advised to change it to a new one using this temporary password. \n\nPassword:.......\n\nThis password will expire after 60 minutes.\nPlease ignore if you did not request for password recovery.\n"
    #     },
    #     {
    #         "topic": "No solve for a week",
    #         "template_name": "no_solve_for_a_week",
    #         "subject": "Zero solve in a week",
    #         "message": "Hello user,\nYou have solved zero problems in the Bootcamp contests in the last 7 days. Please be informed that no solves for two consecutive weeks can cause elimination from this camp.\n"
    #     },
    #     {
    #         "topic": "Very few solves",
    #         "template_name": "very_few_solves",
    #         "subject": "Less than %d solves in a week",
    #         "message": "Hello user,\nYou have not fulfilled the weekly solve requirement in the Bootcamp contests. Please be informed that less than %d solves for two consecutive weeks can cause elimination from this camp.\n"
    #     },
    #     {
    #         "topic": "Kick mail",
    #         "template_name": "kick_mail",
    #         "subject": "Elimination from Bootcamp",
    #         "message": "Hello user,\nWe are sorry to inform you that you have been eliminated from this Bootcamp for failing to fulfill the solve requirements.\n\nFor joining the next season of Bootcamp, please follow our Facebook official page.\n"
    #     },
    #     {
    #         "topic": "Congratulation mail",
    #         "template_name": "congratulation_mail",
    #         "subject": "Congratulations!",
    #         "message": "Hello user, \nCongratulations! You have successfully graduated from Bootcamp and have officially become a rated member of NSUPS.\n\nGood luck on your new journey!\n"
    #     },
    #     {
    #         "topic": "Sorry mail",
    #         "template_name": "sorry_mail",
    #         "subject": "Thanks for your participation!",
    #         "message": "Hello user, \nWe are sorry to inform you that you have not graduated from Bootcamp. \n\nThanks for your participation in this season.\n\nFor joining the next season of Bootcamp, please follow our Facebook official page.\n"
    #     }
    # ]
    # for template in mail_templates:
    #     data = MailTemplate(**template)
    #     data.delete_from_db()
    #     data.save_to_mongo()


