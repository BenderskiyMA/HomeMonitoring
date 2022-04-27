import logging
import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from typing import Any, Tuple

from flask_restful.utils import cors

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
from resources.value import Value, ValueOld
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
def check_if_token_in_blacklist(jwt_header: Any, jwt_payload: dict) -> bool:
    return jwt_payload['jti'] in BLACKLIST


@jwt.additional_claims_loader
def add_claims_to_jwt(identity: int) -> dict:
    user = UserModel.find_by_id(identity)
    if user and user.userRole == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback(jwt_header: Any, jwt_data: Any) -> Tuple:
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error: Any) -> Tuple:
    return jsonify({
        'description': 'Signature verification error.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def unauthorized_token_callback(error: Any) -> Tuple:
    return jsonify({
        'description': 'No token provided.',
        'error': 'unauthorized'
    }), 401


@jwt.needs_fresh_token_loader
def fresh_token_need_callback(jwt_header: Any, jwt_data: Any) -> Tuple:
    return jsonify({
        'description': 'The token need to be fresh.',
        'error': 'fresh_token_need'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header: Any, jwt_data: Any) -> Tuple:
    return jsonify({
        'description': 'The token was revoked.',
        'error': 'token_revoked'
    }), 401


@jwt.additional_claims_loader
def add_claims_to_jwt(identity: int) -> dict:
    user = UserModel.find_by_id(identity)
    if user is not None:
        if user.userRole == 1:
            return {'is_admin': True}
        return {'is_admin': False}


api.add_resource(Sensor, '/api/sensor/<int:sensorId>')
api.add_resource(Sensors, '/api/sensors')
api.add_resource(Location, '/api/location/<int:locationID>')
api.add_resource(Locations, '/api/locations')
api.add_resource(ValueOld, '/monitoring/data/')
api.add_resource(Value, '/api/value/<string:sensorId>')
api.add_resource(Values, '/api/data/<int:sensorId>/<string:periodType>',
                         '/api/values/<int:sensorId>/<string:periodType>',
                         '/api/data/<int:sensorId>/<string:periodType>/',
                         '/api/values/<int:sensorId>/<string:periodType>/')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(SetupAdmin, '/setupadmin')
api.add_resource(UserManage, '/usermanage/<string:username>')
