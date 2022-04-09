from typing import Tuple

from flask_restful import Resource
from model.user import UserModel
from utils.paramparsers import _user_parser


class SetupAdmin(Resource):
    def post(self) -> Tuple:
        data = _user_parser.parse_args()

        if UserModel.get_user_count() == 0:
            user = UserModel(data["username"], data["password"])
            user.userRole = 1
            user.save_to_db()
            return {"message": "Admin user created."}, 201

        return {"message": "Error, database already contain user."}, 400


