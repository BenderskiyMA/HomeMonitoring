from typing import Tuple

from flask_restful import Resource
from flask_jwt_extended import jwt_required,  get_jwt_identity, create_access_token


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self) -> Tuple:
        current_user: int = get_jwt_identity()
        new_token: str = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token
                }, 200
