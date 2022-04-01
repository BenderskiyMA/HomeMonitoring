import datetime

from flask import jsonify
from sqlalchemy.sql.functions import now

from db import db


class SensorModel(db.Model):
    __tablename__ = "sensors"
    id = db.Column(db.Integer, primary_key=True)
    sensorName = db.Column(db.String(255))
    unitName = db.Column(db.String(50))
    maxVal = db.Column(db.Float(precision=2), default=100.00)
    minVal = db.Column(db.Float(precision=2), default=-1000.00)
    locationID = db.Column(db.Integer, db.ForeignKey('locations.id'))
    sourceList = db.Column(db.String(1024))
    sensorMAC = db.Column(db.String(50), nullable=False)
    sensorType = db.Column(db.String(10), default="temp")
    lastGoodValue = db.Column(db.Float(precision=2), nullable=False, default=0.00)
    lastGoodValueTime = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
    updateRate = db.Column(db.Integer, default=1)

    location = db.relationship('LocationModel')

    def __init__(self, sensorName: str,
                 unitName: str,
                 maxVal: float,
                 minVal: float,
                 locationId: int,
                 sourceList: str,
                 sensorMAC: str,
                 sensorType: str,
                 updateRate: int):
        self.sensorName = sensorName
        self.unitName = unitName
        self.maxVal = maxVal
        self.minVal = minVal
        self.locationID = locationId
        self.sourceList = sourceList,
        self.sensorMAC = sensorMAC,
        self.sensorType = sensorType,
        self.lastGoodValue = 0,
        self.updateRate = updateRate

    def json(self):
        """
                "id": 10,
                "sensorName": "Температура в кессоне. Верх",
                "sensorType": "temp",
                "sensorUnitName": "celsius",
                "sensorMaxValue": 100.0,
                "sensorMinValue": -100.0,
                "updateRate": 1,
                "lastGoodValue": 0.56,
                "lastGoodValueMoment": "2022-04-01T15:28:29.000+00:00",
                "locationID": 1,
                "locationName": "Дача",
                "sourceList": "*",
                "sensorIdentifier": "ESPBCFF4D82893FT1",
                "changedState": false
        """
        result = {"id": self.id,
                  "sensorName": self.sensorName,
                  "sensorUnitName": self.unitName,
                  "sensorMaxValue": self.maxVal,
                  "sensorMinValue": self.minVal,
                  "locationID": self.locationID,
                  "locationName": self.location.locationName,
                  "sourceList": self.sourceList,
                  "sensorIdentifier": self.sensorMAC,
                  "sensorType": self.sensorType,
                  "lastGoodValue": self.lastGoodValue,
                  "lastGoodValueMoment": self.lastGoodValueTime.isoformat(),
                  "updateRate": self.updateRate,
                  "changedState": False
                  }
        return result

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_sensorid(cls, sensorid: str):
        return cls.query.filter_by(sensorMAC=sensorid).first()

    @classmethod
    def find_by_location_id(cls, _locationid: int):
        return cls.query.filter_by(locationID=_locationid).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
