from flask_restful import reqparse

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
_sensor_parser.add_argument("unitName",
                            type=str,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("maxVal",
                            type=float,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("minVal",
                            type=str,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("locationId",
                            type=int,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("sourceList",
                            type=str,
                            required=True,
                            help="This field can not be blank!"
                            )

_sensor_parser.add_argument("sensorMAC",
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
