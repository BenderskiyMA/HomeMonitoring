from datetime import datetime, timedelta

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from model.sensor import SensorModel
from model.value import ValueModel
from utils.functions import isfloat, getfloat, checkrange

_value_parser = reqparse.RequestParser()
_value_parser.add_argument("act",
                           type=str,
                           required=True,
                           help="This field can not be blank!"
                           )
_value_parser.add_argument("data",
                           type=str,
                           required=True,
                           help="This field can not be blank!"
                           )


class Value(Resource):

    def get(self):
        # Parse following data(act=add and miltiline sensorid$value pairs)
        # http://localhost:8080/data/?act=add&data=4535234523$238
        # 23412421433$4.3
        # 45352345235$-4.5
        # 252523523$-6
        # 232222222$73
        data = _value_parser.parse_args()
        errtext = ""
        errcode = 200

        if data["act"] == "add":
            for line in data["data"].split("\n"):
                (sensorid, value) = line.split("$")

                if sensorid and value and isfloat(value):
                    fv = getfloat(value)
                    s = SensorModel.find_by_sensorid(sensorid)
                    if s:
                        lt = s.lastGoodValueTime + timedelta(minutes=s.updateRate)
                        nt = datetime.now()
                        if lt < nt:
                            # Time delta is valid, check the value
                            v = ValueModel(fv, True, s.id)
                            if v:
                                if not checkrange(fv, s.minVal, s.maxVal):
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
                    return {"message": "Error! Can not parse data string {}.".format(data["data"])}, 500
            return errtext, errcode
        else:
            return {"message": "Error! Invalid act value: {}".format(data["act"])}, 500
