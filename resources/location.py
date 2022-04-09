from typing import Tuple

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from model.location import LocationModel
from utils.functions import ERROR_ACCESS_DENIED, is_admin
from utils.paramparsers import _location_parser


class Location(Resource):

    @jwt_required(fresh=True)
    def get(self, locationID: int) -> Tuple:
        if not is_admin():
            return ERROR_ACCESS_DENIED, 403
        location = LocationModel.find_by_id(locationID)
        if location is None:
            return {"Message": "Error! Location not found."}, 404
        return location.json()

    @jwt_required(fresh=True)
    def post(self, locationID: int) -> Tuple:
        if not is_admin():
            return ERROR_ACCESS_DENIED, 403
        data = _location_parser.parse_args()
        if LocationModel.find_by_name(data["locationName"]):
            return {"Message": "Error! Location already exists '{}'.".format(data["locationName"])}, 400
        try:
            LocationModel(data["locationName"], data["locationCoordinates"]).save_to_db()
            return {"Message": "Location created."}, 201
        except Exception as E:
            return {"Message": "Error occurred. {}".format(E)}, 500

    @jwt_required(fresh=True)
    def put(self, locationID: int) -> Tuple:
        if not is_admin():
            return ERROR_ACCESS_DENIED, 403
        data = _location_parser.parse_args()
        location = LocationModel.find_by_id(locationID)
        if location is None:
            return {"Message": "Error! Location not found."}, 400
        locationnew = LocationModel.find_by_name(data["locationName"])
        if (locationnew is not None) and not (location.id == locationnew.id):
            return {"Message": "Error! Location already exists '{}'.".format(data["locationName"])}, 400
        try:
            location.locationCoordinates = data["locationCoordinates"]
            location.locationName = data["locationName"]
            location.save_to_db()
            return location.json(), 201
        except Exception as E:
            return {"Message": "Error occurred. {}".format(E)}, 500

    @jwt_required(fresh=True)
    def delete(self, locationID: int) -> Tuple:
        if not is_admin():
            return ERROR_ACCESS_DENIED, 403
        try:
            LocationModel.find_by_id(locationID).delete()
            return {"Message": "Location deleted."}, 200
        except Exception as E:
            return {"Message": "Error occurred. {}".format(E)}, 500

