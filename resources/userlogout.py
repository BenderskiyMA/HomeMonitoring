from typing import Tuple

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity
from model.user import UserModel
from resources.blacklist import BLACKLIST


class UserLogout(Resource):
    @jwt_required()
    def post(self) -> Tuple:
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {"Message": "success logged out."}


