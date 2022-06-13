from typing import Tuple

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from model.sensor import SensorModel
from utils.functions import is_admin, ERROR_ACCESS_DENIED


class Sensors(Resource):
    # @jwt_required(fresh=True)
    def get(self) -> Tuple:
        # if not is_admin():
        #    return ERROR_ACCESS_DENIED, 403
        sensors: list = [x.json() for x in SensorModel.find_all_except_hidden()]
        return sensors, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return {'Allow': 'GET'}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET',
                                       'Access-Control-Allow-Headers': 'Access-Control-Allow-Headers, Origin,Accept, '
                                                                       'X-Requested-With, Content-Type, '
                                                                       'Access-Control-Request-Method, '
                                                                       'Access-Control-Request-Headers'}


class AllSensors(Resource):
    # @jwt_required(fresh=True)
    def get(self) -> Tuple:
        # if not is_admin():
        #    return ERROR_ACCESS_DENIED, 403
        sensors: list = [x.json() for x in SensorModel.find_all()]
        return sensors, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return {'Allow': 'GET'}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET',
                                       'Access-Control-Allow-Headers': 'Access-Control-Allow-Headers, Origin,Accept, '
                                                                       'X-Requested-With, Content-Type, '
                                                                       'Access-Control-Request-Method, '
                                                                       'Access-Control-Request-Headers'}
