from db import db


class LocationModel(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    locationName = db.Column(db.String(255))
    locationCoordinates = db.Column(db.String(255))

    def __init__(self, locationName: str, locationCoordinates: str):
        self.locationName = locationName
        self.locationCoordinates = locationCoordinates

    def json(self):
        return {"id": self.id,
                "locationName": self.locationName,
                "locationCoordinates": self.locationCoordinates,
                }

    @classmethod
    def find_by_name(cls, locationName: str):
        return cls.query.filter_by(locationName=locationName).first()

    @classmethod
    def find_by_id(cls, locationId: int):
        return cls.query.filter_by(id=locationId).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
