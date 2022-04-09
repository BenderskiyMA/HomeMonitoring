from typing import Tuple

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from model.user import UserModel
from utils.functions import is_admin
from utils.paramparsers import _user_parser





class UserManage(Resource):
    @jwt_required(fresh=True)
    def post(self, username: str) -> Tuple:

        if not is_admin():
            return {"message": "Admin privilege required."}, 401
        data = _user_parser.parse_args()
        if data["userrole"] is None:
            data["userrole"] = 0
        if UserModel.find_by_name(username):
            return {"message": "Error! User exists, use PUT or DELETE method"}, 400
        user = UserModel(username, data["password"])
        user.userRole = data["userrole"]
        user.save_to_db()
        return {"message": "User created."}, 201

    @jwt_required(fresh=True)
    def put(self, username: str) -> Tuple:
        if not is_admin():
            return {"message": "Admin privilege required."}, 401
        data = _user_parser.parse_args()
        if data["userrole"] is None:
            data["userrole"] = 0
        user = UserModel.find_by_name(username)
        new = False
        if user is None:
            user = UserModel(username, data["password"])
            new = True
        else:
            user.setpassword(data["password"])
        if not new and user.userRole == 1 and UserModel.get_admin_count() == 1 and data["userrole"] == 0:
            return {"message": "Error! Can not set to simple last admin user!"}

        user.userRole = data["userrole"]
        user.save_to_db()
        if new:
            return {"message": "User created."}, 201
        else:
            return {"message": "User modified."}, 201

    @jwt_required(fresh=True)
    def delete(self, username: str) -> Tuple:
        if not is_admin():
            return {"message": "Admin privilege required."}, 401
        data = _user_parser.parse_args()
        user = UserModel.find_by_name(username)
        if user is None:
            return {"message": "Error! User does not exist."}, 400
        else:
            if UserModel.get_user_count() > 1:
                if (user.userRole == 1 and UserModel.get_admin_count() > 1) or user.userRole == 0:
                    user.delete()
                else:
                    return {"message": "Error! Can not delete last Admin user."}, 400
            else:
                return {"message": "Error! Can not delete last user."}, 400
        return {"message": "User deleted."}
