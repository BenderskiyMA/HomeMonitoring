from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity
from model.sensor import SensorModel


class Sensors(Resource):
    pass
