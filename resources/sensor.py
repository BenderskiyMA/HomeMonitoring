import json
from typing import Tuple

from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from model.sensor import SensorModel
from model.value import ValueModel
from utils.functions import is_admin, ERROR_ACCESS_DENIED
from utils.paramparsers import _sensor_parser


class Sensor(Resource):

    @jwt_required(fresh=True)
    def get(self, sensorId: int) -> Tuple:
        if is_admin():
            sensor: SensorModel = SensorModel.find_by_id(sensorId)
            if sensor is None:
                return {"message": "Error! Sensor not found."}, 404
            else:
                return sensor.json(), 200

        else:
            return ERROR_ACCESS_DENIED, 403

    @jwt_required(fresh=True)
    def delete(self, sensorId: int) -> Tuple:
        if is_admin():
            try:
                sensor: SensorModel = SensorModel.find_by_id(sensorId)
                if sensor:
                    ValueModel.delete_by_sensor_id(sensorId=sensor.id)
                    sensor.delete()
                else:
                    return {"Message": "Error! Sensor not found."}, 404
            except Exception as E:
                return {"Message": "Error occurred. {}".format(E)}, 500
            return {"Message": "Sensor and it's values deleted."}, 200
        else:
            return ERROR_ACCESS_DENIED, 403

    @jwt_required(fresh=True)
    def post(self, sensorId: int) -> Tuple:
        if is_admin():
            data: dict = _sensor_parser.parse_args()
            if data["sensorIdentifier"] and SensorModel.find_by_sensorid(data["sensorIdentifier"]):
                return {"Message": "Error! Sensor with sensorMAC '{}' already exists.".format(
                    data["sensorIdentifier"])}, 400
            del data["id"]
            sensor: SensorModel = SensorModel(data
                                              # sensorName=data["sensorName"],
                                              # sensorType=data["sensorType"],
                                              # sensorUnitName=data["sensorUnitName"],
                                              # sensorMaxValue=data["sensorMaxValue"],
                                              # sensorMinValue=data["sensorMinValue"],
                                              # updateRate=data["updateRate"],
                                              # locationID=data["locationID"],
                                              # sourceList=data["sourceList"],
                                              # sensorIdentifier=data["sensorIdentifier"],
                                              # showInList=data["showInList"]
                                              )
            sensor.save_to_db()
            return {"Message": "Sensor added."}, 201

        else:
            return ERROR_ACCESS_DENIED, 403

    @jwt_required(fresh=True)
    def put(self, sensorId: int) -> Tuple:
        if is_admin():
            data: dict = _sensor_parser.parse_args()
            sensor: SensorModel = SensorModel.find_by_sensorid(data["sensorIdentifier"])
            try:
                if sensor:
                    # KEEP id, sensorMAC, lastGoodValue

                    sensor.sensorName = data["sensorName"]
                    sensor.unitName = data["sensorUnitName"]
                    sensor.maxVal = data["sensorMaxValue"]
                    sensor.minVal = data["sensorMinValue"]
                    sensor.locationID = data["locationID"]
                    sensor.sourceList = data["sourceList"]
                    sensor.sensorType = data["sensorType"]
                    sensor.updateRate = data["updateRate"]
                    sensor.showInList = data["showInList"]
                    sensor.save_to_db()
                else:
                    del data["id"]
                    sensor = SensorModel(data)
                    sensor.save_to_db()
                return sensor.json(), 200
            except Exception as E:
                return {"Message": "Error occurred. {}".format(E)}, 500
        else:
            return ERROR_ACCESS_DENIED, 403
