from db import db
from hashlib import sha256


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(255))
    userPassword = db.Column(db.String(255))
    userRole = db.Column(db.Integer, default=0)

    def __init__(self, userName: str, userPassword: str):
        self.userName = userName
        self.userPassword = sha256(userPassword).hexdigest()

    def json(self):
        return {"id": self.id,
                "userName": self.userName,
                "userRole": self.userRole,
                }

    @classmethod
    def find_by_name(cls, userName: str):
        return cls.query.filter_by(userName=userName).first()

    @classmethod
    def find_by_id(cls, userId: int):
        return cls.query.filter_by(id=userId).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
