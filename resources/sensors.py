from typing import Tuple

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from model.sensor import SensorModel
from utils.functions import is_admin, ERROR_ACCESS_DENIED


class Sensors(Resource):
    @jwt_required(fresh=True)
    def get(self) -> Tuple:
        if not is_admin():
            return ERROR_ACCESS_DENIED, 403
        sensors = [x.json() for x in SensorModel.find_all()]
        return sensors, 200
