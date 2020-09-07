from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import *
from common.database import Database
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
app.secret_key = "abcdxyz"

api = Api(app)
jwt = JWTManager(app)
CORS(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if UserModel.get_by_username(identity).is_admin:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST  # Here we blacklist particular JWTs that have been created in the past.


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(Lookup, "/lookup")
api.add_resource(UserFromToken, "/userinfo")


@app.before_first_request
def initialize_database():
    Database.initialize()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
