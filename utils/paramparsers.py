from flask_restful import reqparse
from flask_restful.reqparse import RequestParser

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
                          type=str,
                          required=False,
                          help="This field can not be blank!"
                          )
_user_parser.add_argument("password",
                          type=str,
                          required=True,
                          help="This field can not be blank!"
                          )
_user_parser.add_argument("userrole",
                          type=int,
                          required=False,
                          help="This field must be 0 for simple user or more for admin!"
                          )
"""
"sensorName": self.sensorName,
"unitName": self.unitName,
"maxval": self.maxVal,
"minval": self.minVal,
"locationID": self.locationID,
"sourceList": self.sourceList,
"sensorMAC": self.sensorMAC,
"sensorType": self.sensorType,
"lastGoodValue": self.lastGoodValue,
"lastGoodValueTime": self.lastGoodValueTime,
"updateRate": self.updateRate
"showInList": self.showInList
})
"""

_sensor_parser = reqparse.RequestParser()
_sensor_parser.add_argument("id",
                            type=int,
                            required=False,
                            )

_sensor_parser.add_argument("sensorName",
                            type=str,
                            required=True,
                            help="This field can not be blank!"
                            )
_sensor_parser.add_argument("sensorUnitName",
                            type=str,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("sensorMaxValue",
                            type=float,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("sensorMinValue",
                            type=str,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("locationID",
                            type=int,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("sourceList",
                            type=str,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("sensorIdentifier",
                            type=str,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("sensorType",
                            type=str,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("updateRate",
                            type=int,
                            required=True,
                            help="This field can not be blank!"
                            )
_sensor_parser.add_argument("showInList",
                            type=bool,
                            required=True,
                            help="This field can not be blank!"
                            )

_location_parser: RequestParser = reqparse.RequestParser()
_location_parser.add_argument("id",
                              type=int,
                              required=False,
                              )

_location_parser.add_argument("locationName",
                              type=str,
                              required=True,
                              help="This field can not be blank!"
                              )

_location_parser.add_argument("locationCoordinates",
                              type=str,
                              required=False,
                              help="This field can not be blank!"
                              )

_old_value_parser = reqparse.RequestParser()
_old_value_parser.add_argument("act",
                               type=str,
                               required=True,
                               help="This field can not be blank!"
                               )
_old_value_parser.add_argument("data",
                               type=str,
                               required=True,
                               help="This field can not be blank!"
                               )

_value_parser = reqparse.RequestParser()
_value_parser.add_argument("value",
                           type=float,
                           required=True,
                           help="This field can not be blank!"
                           )
