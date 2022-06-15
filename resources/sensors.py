from typing import Tuple, List

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from model.sensor import SensorModel
from utils.functions import is_admin, ERROR_ACCESS_DENIED


class Sensors(Resource):
    # @jwt_required(fresh=True)
    def get(self) -> Tuple:
        """This method returns only those sensors, that contain true in showInList field. Use it for UI purposes."""
        # if not is_admin():
        #    return ERROR_ACCESS_DENIED, 403
        sensors: List = [x.json() for x in SensorModel.find_all_except_hidden()]
        return sensors, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self) -> Tuple:
        """This method returns headers for CORS (in case of different endpoints of UI and API)"""
        return {'Allow': 'GET'}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET',
                                       'Access-Control-Allow-Headers': 'Access-Control-Allow-Headers, Origin,Accept, '
                                                                       'X-Requested-With, Content-Type, '
                                                                       'Access-Control-Request-Method, '
                                                                       'Access-Control-Request-Headers'}


class AllSensors(Resource):
    # @jwt_required(fresh=True)
    def get(self) -> Tuple:
        """This method returns all Sensors (use it for admin page)"""
        # if not is_admin():
        #    return ERROR_ACCESS_DENIED, 403
        sensors: list = [x.json() for x in SensorModel.find_all()]
        return sensors, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self) -> Tuple:
        """This method returns headers for CORS (in case of different endpoints of UI and API)"""
        return {'Allow': 'GET'}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET',
                                       'Access-Control-Allow-Headers': 'Access-Control-Allow-Headers, Origin,Accept, '
                                                                       'X-Requested-With, Content-Type, '
                                                                       'Access-Control-Request-Method, '
                                                                       'Access-Control-Request-Headers'}
