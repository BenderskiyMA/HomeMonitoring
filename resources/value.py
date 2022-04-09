from datetime import datetime, timedelta

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from model.sensor import SensorModel
from model.value import ValueModel
from utils.functions import isfloat, getfloat, checkvalueinrange
from utils.paramparsers import _old_value_parser, _value_parser


class ValueOld(Resource):

    # Old API for old sensors
    # adding via GET String like narodmon.ru project
    def get(self):
        # Parse following data(act=add and miltiline sensorid$value pairs)
        # http://localhost:8080/data/?act=add&data=4535234523$238
        # 23412421433$4.3
        # 45352345235$-4.5
        # 252523523$-6
        # 232222222$73
        data = _old_value_parser.parse_args()
        errtext = ""
        errcode = 200

        if data["act"] == "add":
            for line in data["data"].split("\n"):
                (sensorid, value) = line.split("$")
                if sensorid and value and isfloat(value):
                    fv = getfloat(value)
                    if fv:
                        s = SensorModel.find_by_sensorid(sensorid)
                        if s:
                            lt = s.lastGoodValueTime + timedelta(minutes=s.updateRate)
                            nt = datetime.now()
                            if lt < nt:
                                # Time delta is valid, check the value
                                v = ValueModel(fv, True, s.id)
                                if v:
                                    if not checkvalueinrange(fv, s.minVal, s.maxVal):
                                        v.valid = False
                                    else:
                                        s.lastGoodValue = fv
                                        s.lastGoodValueTime = nt
                                        s.save_to_db()
                                    v.save_to_db()
                                    errtext = s.updateRate
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
    def post(self, sensorId: str):
        data = _value_parser.parse_args()
        sensor = SensorModel.find_by_sensorid(sensorId)
        if sensor and data["value"] and isfloat(data["value"]):
            fv = getfloat(data["value"])
            lt = sensor.lastGoodValueTime + timedelta(minutes=sensor.updateRate)
            nt = datetime.now()
            if lt < nt:
                # Time delta is valid, check the value
                v = ValueModel(fv, True, sensor.id)
                if v:
                    if not checkvalueinrange(fv, sensor.minVal, sensor.maxVal):
                        v.valid = False
                    else:
                        sensor.lastGoodValue = fv
                        sensor.lastGoodValueTime = nt
                        sensor.save_to_db()
                    v.save_to_db()
                    return sensor.updateRate, 200
                else:
                    return {"message": "Request has one or more Errors! Can not create ValueModel "
                                       "object."}, 500
            else:
                return {"message": "Request has one or more Errors! Too many requests."}, 400
        else:
            return {"message": "Request has one or more Errors! Can not find Sensor object with id {}.".format(
                sensorId)}, 500
