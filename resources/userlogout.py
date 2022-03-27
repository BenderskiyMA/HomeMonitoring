from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity
from model.user import UserModel


class UserLogout(Resource):
    pass


