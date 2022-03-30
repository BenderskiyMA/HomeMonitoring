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
        result = {"id": self.id,
                          "sensorName": self.sensorName,
                          "unitName": self.unitName,
                          "maxVal": self.maxVal,
                          "minVal": self.minVal,
                          "locationId": self.locationID,
                          "sourceList": self.sourceList,
                          "sensorMAC": self.sensorMAC,
                          "sensorType": self.sensorType,
                          "lastGoodValue": self.lastGoodValue,
                          "lastGoodValueTime":  self.lastGoodValueTime.isoformat(),
                          "updateRate": self.updateRate
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
