import datetime
from flask import jsonify

from db import db


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
                        "valis": self.valid,
                        "sensorId": self.sensorId,
                        })

    @classmethod
    def find_by_sensor_id_from_to_one_values(cls, sensorId: int,
                                             fromDate: datetime,
                                             toDate: datetime):
        # hour and day, one value
        pass

    @classmethod
    def find_by_sensor_id_from_to_two_values_week(cls, sensorId: int,
                                                  fromDate: datetime,
                                                  toDate: datetime):
        # week, two values
        pass

    @classmethod
    def find_by_sensor_id_from_to_two_values_month(cls, sensorId: int,
                                                   fromDate: datetime,
                                                   toDate: datetime):
        # month, two values
        pass

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_by_sensor_id(cls, sensorId: int):
        cls.query.filter_by(sensorId=sensorId).delete()
        db.session.commit()
