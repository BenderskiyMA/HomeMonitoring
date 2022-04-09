from typing import Tuple

from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import safe_str_cmp

from model.user import UserModel
from utils.paramparsers import _user_parser


class UserLogin(Resource):
    @classmethod
    def post(cls) -> Tuple:
        # get data from  parser
        data = _user_parser.parse_args()
        if data["username"] is None:
            return {"message": "Invalid credentials"}, 401
        # find user in database
        user = UserModel.find_by_name(data["username"])
        # check password
        if user and safe_str_cmp(user.userPassword, UserModel.encodepassword(data["password"])):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {'access_token': access_token,
                    'refresh_token': refresh_token}, 200
        return {"message": "Invalid credentials"}, 401
