import datetime
from typing import List

from flask import jsonify, Response
from sqlalchemy import String

from db import db
from sqlalchemy.sql import text


class ValueModel(db.Model):
    __tablename__ = "vals"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float(precision=2), default=0.00)
    value2: float = 0
    createTimeStamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
    valid = db.Column(db.Boolean, default=True)
    sensorId = db.Column(db.Integer, db.ForeignKey('sensors.id'))

    sensor = db.relationship('SensorModel')

    def __init__(self, value: float, valid: bool, sensorId: int):
        self.value = value
        self.valid = valid
        self.sensorId = sensorId

    def json(self):
        return jsonify({"id": self.id,
                        "value": self.value,
                        "value2": self.value2,
                        "createTimeStamp": self.createTimeStamp,
                        "valid": self.valid,
                        "sensorId": self.sensorId,
                        })
    # [{"sensorID":10,"value":1.12,"value2":0.0,"moment":"2022-04-26T16:48:45.000+00:00","updateRate":0,"valid":true}

    @classmethod
    def find_values_for_prepared_statement(cls, sensorId: int, fromDate: datetime, toDate: datetime,
                                           statement: str) -> list:
        params: dict = {"sensorid": sensorId,
                        "fromdate": fromDate,
                        "todate": toDate}
        queryresult = db.engine.execute(statement, params)
        return [{"value": float(row["maxval"]),
                 "value2": float(row["value"]),
                 "moment": row["createTimeStamp"].isoformat(),
                 "sensorID": sensorId,
                 "updateRate": 0,
                 "valid": True
                 } for row in queryresult]

    @classmethod
    def find_by_sensor_id_from_to_one_values(cls, sensorId: int,
                                             fromDate: datetime,
                                             toDate: datetime) -> list:
        # hour and day, one value
        statement: str = db.text("SELECT  id,value as maxval,value,createTimeStamp,valid FROM vals where "
                                 "sensorID=:sensorid and createtimestamp >=:fromdate and "
                                 "createtimestamp<=:todate  and valid=TRUE order by "
                                 "createTimeStamp")
        result = cls.find_values_for_prepared_statement(sensorId, fromDate, toDate, statement)
        return result

    @classmethod
    def find_by_sensor_id_from_to_two_values_week(cls, sensorId: int,
                                                  fromDate: datetime,
                                                  toDate: datetime) -> list:
        # week, two values
        statement: str = db.text("SELECT createTimeStamp,max(value) as maxval,min(value) as value,T_YEAR,T_MONTH,T_DAY,"
                                 "T_HOUR from vals where sensorID=:sensorid and valid=true and "
                                 "createtimestamp>=:fromdate and createtimestamp<=:todate group by "
                                 "T_YEAR,T_MONTH,T_DAY,T_HOUR order by createTimeStamp")
        return cls.find_values_for_prepared_statement(sensorId, fromDate, toDate, statement)

    @classmethod
    def find_by_sensor_id_from_to_two_values_month(cls, sensorId: int,
                                                   fromDate: datetime,
                                                   toDate: datetime) -> list:
        # month, two values
        statement: str = db.text("SELECT createTimeStamp,max(value) as maxval,min(value) as value,T_YEAR,T_MONTH,T_DAY"
                                 " from vals where sensorID=:sensorid and valid=true and createtimestamp>=:fromdate and"
                                 " createtimestamp<=:todate group by T_YEAR,T_MONTH,T_DAY order by createTimeStamp")
        return cls.find_values_for_prepared_statement(sensorId, fromDate, toDate, statement)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_by_sensor_id(cls, sensorId: int):
        cls.query.filter_by(sensorId=sensorId).delete()
        db.session.commit()
