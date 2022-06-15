from typing import Dict

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
    showInList = db.Column(db.Boolean, default=True)

    location = db.relationship('LocationModel')

    def __init__(self, data: Dict):
        self.sensorName = data["sensorName"]
        self.unitName = data["sensorUnitName"]
        self.maxVal = data["sensorMaxValue"]
        self.minVal = data["sensorMinValue"]
        self.locationID = data["locationID"]
        self.sourceList = data["sourceList"]
        self.sensorMAC = data["sensorIdentifier"]
        self.sensorType = data["sensorType"]
        self.lastGoodValue = 0
        self.updateRate = data["updateRate"]
        self.showInList = data["showInList"]

    def json(self) -> Dict:
        """Returns JSON representation of the class"""
        return {"id": self.id,
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
                "changedState": False,
                "showInList": self.showInList
                }

    @classmethod
    def find_by_id(cls, _id: int):
        """Returns SensorModel object with id=_id"""
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_sensorid(cls, sensorid: str):
        """Returns SensorModel object with sensorMAC=sensorid"""
        return cls.query.filter_by(sensorMAC=sensorid).first()

    @classmethod
    def find_by_location_id(cls, _locationid: int):
        """Returns list of all sensors with locationID=_locationid."""
        return cls.query.filter_by(locationID=_locationid).all()

    @classmethod
    def find_by_location_id_except_hidden(cls, _locationid: int):
        """Returns list of all sensors with locationID=_locationid and showInList=True."""
        return cls.query.filter_by(locationID=_locationid, showInList=True).all()
    @classmethod
    def find_all(cls):
        """Returns list of all sensors."""
        return cls.query.all()

    @classmethod
    def find_all_except_hidden(cls):
        """Returns list of sensors with showInList=True."""
        return cls.query.filter_by(showInList=True)

    def save_to_db(self):
        """Saving object to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete object with id=self.id from database."""
        db.session.delete(self)
        db.session.commit()
