from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from model.value import ValueModel
from model.sensor import SensorModel
from utils.functions import PERIOD_TYPES
from datetime import datetime, timedelta


def gethourvalues(sensorId: int) -> list:
    todate: datetime = datetime.now()
    fromdate = todate - timedelta(hours=1)
    return ValueModel.find_by_sensor_id_from_to_one_values(sensorId, fromdate, todate)


def getdayvalues(sensorId: int) -> list:
    todate: datetime = datetime.now()
    fromdate = todate - timedelta(days=1)
    return ValueModel.find_by_sensor_id_from_to_one_values(sensorId, fromdate, todate)


def getmonthvalues(sensorId: int) -> list:
    todate: datetime = datetime.now()
    fromdate = todate - timedelta(days=30)
    return ValueModel.find_by_sensor_id_from_to_two_values_month(sensorId, fromdate, todate)


def getweekvalues(sensorId: int) -> list:
    todate: datetime = datetime.now()
    fromdate = todate - timedelta(weeks=1)
    return ValueModel.find_by_sensor_id_from_to_two_values_week(sensorId, fromdate, todate)


class Values(Resource):

    # @jwt_required(fresh=True)
    def get(self, sensorId: int, periodType: str) -> tuple:
        sensor = SensorModel.find_by_id(sensorId)
        if sensor is None:
            return {"message": "Sensor with id {} not found.".format(sensorId)}, 404
        # if periodType not in PERIOD_TYPES:
        #    return {"message": "Unknown period type value (only hour|day|week|month are accepted)."}, 400
        return {
            "hour": (gethourvalues(sensorId), 200, {'Access-Control-Allow-Origin': '*'}),
            "day": (getdayvalues(sensorId), 200, {'Access-Control-Allow-Origin': '*'}),
            "week": (getweekvalues(sensorId), 200, {'Access-Control-Allow-Origin': '*'}),
            "month": (getmonthvalues(sensorId), 200, {'Access-Control-Allow-Origin': '*'}),
        }.get(periodType, ({"message": "Unknown period type value (only hour|day|week|month are accepted)."}, 400,
                           {'Access-Control-Allow-Origin': '*'}))

    def options(self, sensorId: int, periodType: str):
        return {'Allow': 'GET'}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET',
                                       'Access-Control-Allow-Headers': 'Access-Control-Allow-Headers, Origin,Accept, '
                                                                       'X-Requested-With, Content-Type, '
                                                                       'Access-Control-Request-Method, '
                                                                       'Access-Control-Request-Headers'}

