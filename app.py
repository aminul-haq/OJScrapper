from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import *
from common.database import Database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
app.secret_key = "abcdxyz"

api = Api(app)
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if UserModel.get_by_username(identity).is_admin:
        return {'is_admin': True}
    return {'is_admin': False}


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(Lookup, "/lookup")


@app.before_first_request
def initialize_database():
    Database.initialize()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
