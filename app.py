import os
from logging import debug

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request

from model.user import UserModel
from resources.blacklist import BLACKLIST
from resources.location import Location
from resources.locations import Locations
from resources.sensor import Sensor
from resources.sensors import Sensors
from resources.setupadmin import SetupAdmin
from resources.tokenrefresh import TokenRefresh
from resources.userlogin import UserLogin
from resources.userlogout import UserLogout
from resources.usermanage import UserManage
from resources.value import Value
from resources.values import Values

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = os.environ.get('jwt_secret_key')
api = Api(app)

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    if user and user.userRole == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification error.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def unauthorized_token_callback(error):
    return jsonify({
        'description': 'No token provided.',
        'error': 'unauthorized'
    }), 401


@jwt.needs_fresh_token_loader
def fresh_token_need_callback(jwt_header, jwt_data):
    return jsonify({
        'description': 'The token need to be fresh.',
        'error': 'fresh_token_need'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return jsonify({
        'description': 'The token was revoked.',
        'error': 'token_revoked'
    }), 401


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    if not user is None:
        if user.userRole == 1:
            return {'is_admin': True}
        return {'is_admin': False}


api.add_resource(Sensor, '/sensor/<int:sensorId>')
api.add_resource(Sensors, '/sensors')
api.add_resource(Location, '/location/<int:locationId>')
api.add_resource(Locations, '/locations')
api.add_resource(Value, '/value')
api.add_resource(Values, '/values/<string:periodType>/')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(SetupAdmin, '/setupadmin')
api.add_resource(UserManage, '/usermanage/<string:username>')

if __name__ == '__main__':
    from db import db

    db.init_app(app)


    @app.before_first_request
    def create_tables():
        db.create_all()


    app.run(port=5000)
