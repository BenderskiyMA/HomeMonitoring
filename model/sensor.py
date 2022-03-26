import datetime

from flask import jsonify

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
                 maxval: float,
                 minval: float,
                 locationID: int,
                 sourceList: str,
                 sensorMAC: str,
                 sensorType: str,
                 lastGoodValue: float,
                 lastGoodValueTime: datetime,
                 updateRate: int):
        self.sensorName = sensorName
        self.unitName = unitName
        self.maxVal = maxval
        self.minVal = minval
        self.locationID = locationID
        self.sourceList = sourceList,
        self.sensorMAC = sensorMAC,
        self.sensorType = sensorType,
        self.lastGoodValue = lastGoodValue,
        self.lastGoodValueTime = lastGoodValueTime,
        self.updateRate = updateRate

    def json(self):
        return jsonify({"id": self.id,
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

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_location_id(cls, _locationid: int):
        return cls.query.filter_by(locationID=_locationid).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
