import json

from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from model.sensor import SensorModel
from model.value import ValueModel
from utils.functions import is_admin, ERROR_ACCESS_DENIED
from utils.paramparsers import _sensor_parser


class GetSensor(Resource):

    @jwt_required(fresh=True)
    def get(self, sensorId: int):
        if is_admin():
            s = SensorModel.find_by_id(sensorId)
            if s is None:
                return {"message": "Error! Sensor not found."}, 404
            else:
                return s.json(), 200

        else:
            return ERROR_ACCESS_DENIED, 403

    @jwt_required(fresh=True)
    def delete(self, sensorId:int):
        if is_admin():
            try:
                s = SensorModel.find_by_id(sensorId)
                if s:
                    ValueModel.delete_by_sensor_id(sensorId=s.id)
                    s.delete()
                else:
                    return {"Message": "Error! Sensor not found."}, 404
            except Exception as E:
                return {"Message": "Error occurred. {}".format(E)}, 500
            return {"Message": "Sensor and it's values deleted."}, 200
        else:
            return ERROR_ACCESS_DENIED, 403


class Sensor(Resource):

    @jwt_required(fresh=True)
    def post(self):
        if is_admin():
            data = _sensor_parser.parse_args()
            if data["sensorMAC"] and SensorModel.find_by_sensorid(data["sensorMAC"]):
                return {"Message": "Error! Sensor with sensorMAC '{}' already exists.".format(data["sensorMAC"])}, 400
            del data["id"]
            s = SensorModel(**data)
            s.save_to_db()
            return {"Message": "Sensor added."}, 201

        else:
            return ERROR_ACCESS_DENIED, 403

    @jwt_required(fresh=True)
    def put(self):
        if is_admin():
            data = _sensor_parser.parse_args()
            s = SensorModel.find_by_sensorid(data["sensorMAC"])
            try:
                if s:
                    # KEEP id, sensorMAC, lastGoodValue
                    s.sensorName = data["sensorName"]
                    s.unitName = data["unitName"]
                    s.maxVal = data["maxVal"]
                    s.minVal = data["minVal"]
                    s.locationID = data["locationId"]
                    s.sourceList = data["sourceList"]
                    s.sensorType = data["sensorType"]
                    s.updateRate = data["updateRate"]
                    s.save_to_db()
                else:
                    del data["id"]
                    s = SensorModel(**data)
                    s.save_to_db()
                return s.json(), 200
            except Exception as E:
                return {"Message": "Error occurred. {}".format(E)}, 500
        else:
            return ERROR_ACCESS_DENIED, 403

