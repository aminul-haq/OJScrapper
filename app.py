from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user_resource import *
from resources.classroom_resource import *
from resources.student_resource import *
from resources.dashboard_resource import *
from resources.admin_panel_resources import *
from common.database import Database
from common import solve_updater
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
app.config["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"] = 1440
app.secret_key = "abcdxyz"

api = Api(app)
jwt = JWTManager(app)
CORS(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.get_by_username(identity)
    if user and user.is_admin:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST  # Here we blacklist particular JWTs that have been created in the past.


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(Lookup, "/lookup")
api.add_resource(UserInfo, "/userinfo")
api.add_resource(OJUpdate, "/ojupdate")
api.add_resource(Classroom, "/classroom")
api.add_resource(CreateClassroom, "/createclass")
api.add_resource(Student, "/student")
api.add_resource(ClassRankList, "/classrank")
api.add_resource(Dashboard, "/dashboard")
api.add_resource(ContestData, "/contestdata")
api.add_resource(ClassroomUpdate, "/udpateclassdata")
api.add_resource(DataUpdater, "/updatescheduler")
api.add_resource(EmailSender, "/sendmail")
api.add_resource(Announcements, "/announcements")
api.add_resource(WhitelistEmail, "/whitelist")
api.add_resource(Todos, "/todos")




@app.route("/")
def home():
    return "Hello", 200


@app.route("/servertime")
@jwt_required
def get_server_time():
    return str(datetime.datetime.now()), 200


@app.before_first_request
def initialize_database():
    Database.initialize()
    cron_job.start()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
