from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity
from model.location import LocationModel
from utils.functions import is_admin, ERROR_ACCESS_DENIED


class Locations(Resource):
    @jwt_required(fresh=True)
    def get(self):
        if not is_admin():
            return ERROR_ACCESS_DENIED, 403
        locations = [x.json() for x in LocationModel.find_all()]
        return locations, 200
