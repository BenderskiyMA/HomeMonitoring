from datetime import datetime, timedelta
from typing import Tuple

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from model.sensor import SensorModel
from model.value import ValueModel
from utils import functions

from utils.paramparsers import _old_value_parser, _value_parser


class ValueOld(Resource):

    # Old API for old sensors
    # adding via GET String like narodmon.ru project
    def get(self) -> Tuple:
        # Parse following data(act=add and miltiline sensorid$value pairs)
        # http://localhost:8080/data/?act=add&data=4535234523$238
        # 23412421433$4.3
        # 45352345235$-4.5
        # 252523523$-6
        # 232222222$73
        data = _old_value_parser.parse_args()
        errtext = ""
        errcode: int = 200

        if data["act"] == "add":
            for line in data["data"].split("\n"):
                (sensorid, value) = line.split("$")
                if sensorid and functions.isfloat(value):
                    floatvalue = functions.getfloat(str(value))
                    if floatvalue:
                        sensor = SensorModel.find_by_sensorid(sensorid)
                        if sensor:
                            allowedtime = sensor.lastGoodValueTime + timedelta(minutes=sensor.updateRate)
                            nowtime = datetime.now()
                            if allowedtime < nowtime:
                                # Time delta is valid, check the value
                                newvalue = ValueModel(floatvalue, True, sensor.id)
                                if newvalue:
                                    if functions.checkvaluenotinrange(floatvalue, sensor.minVal, sensor.maxVal):
                                        newvalue.valid = False
                                    else:
                                        sensor.lastGoodValue = floatvalue
                                        sensor.lastGoodValueTime = nowtime
                                        sensor.save_to_db()
                                    newvalue.save_to_db()
                                    errtext = sensor.updateRate
                                    errcode = 200

                                else:
                                    errtext = {"message": "Request has one or more Errors! Can not create ValueModel "
                                                          "object."}
                                    errcode = 500
                            else:
                                errtext = {"message": "Request has one or more Errors! Too many requests."}
                                errcode = 400
                        else:
                            errtext = {"message": "Request has one or more Errors! "
                                                  "Can not find Sensor object with id {}.".format(sensorid)}
                            errcode = 500
                    else:
                        return {"message": "Error! Can not parse data string {}, something fucking wrong with float "
                                           "value.".format(data["data"])}, 500
                else:
                    return {"message": "Error! Can not parse data string {}.".format(data["data"])}, 500
            return errtext, errcode
        else:
            return {"message": "Error! Invalid act value: {}".format(data["act"])}, 500


class Value(Resource):
    # @jwt_required(fresh=True)
    def post(self, sensorId: str) -> Tuple:
        data = _value_parser.parse_args()
        sensor = SensorModel.find_by_sensorid(sensorId)
        if sensor:
            if functions.isfloat(str(data["value"])):
                floatvalue = functions.getfloat(str(data["value"]))
                allowedtime = sensor.lastGoodValueTime + timedelta(minutes=sensor.updateRate)
                nowtime = datetime.now()
                if allowedtime < nowtime:
                    # Time delta is valid, check the value
                    newvalue = ValueModel(floatvalue, True, sensor.id)
                    if newvalue:
                        if functions.checkvaluenotinrange(floatvalue, sensor.minVal, sensor.maxVal):
                            newvalue.valid = False
                        else:
                            sensor.lastGoodValue = floatvalue
                            sensor.lastGoodValueTime = nowtime
                            sensor.save_to_db()
                        newvalue.save_to_db()
                        return sensor.updateRate, 200
                    else:
                        return {"message": "Request has one or more Errors! Can not create ValueModel "
                                           "object."}, 500
                else:
                    return {"message": "Request has one or more Errors! Too many requests."}, 400
            else:
                return {"message": "Error! Can not parse value string '{}', something fucking wrong with float "
                                   "value.".format(data["value"])}, 500
        else:
            return {"message": "Request has one or more Errors! Can not find Sensor object with id {}.".format(
                sensorId)}, 500
