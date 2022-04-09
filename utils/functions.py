from flask_jwt_extended import get_jwt
from psycopg2._psycopg import Boolean

ERROR_ACCESS_DENIED = {"message": "Error! Access denied!"}


def isfloat(num: str) -> bool:
    """Takes a string, representing number (positive  or negative or zero), returns True is it is valid number and
    False  in other cases [THIS FUNCTION FASTER FOR ABOUT 3-5%]"""
    return num.replace(".", "", 1).replace("-", "", 1).isnumeric()


def getfloat(num: str) -> float:
    """Takes a string, representing number (positive  or negative or zero), returns it float value or None"""
    if isfloat(num):
        return float(num)
    else:
        return None


def checkvaluenotinrange(value: float, minVal: float, maxVal: float) -> bool:
    """Takes value, minVal, maxVal floats and check if value in range from minVal(including) to maxVal(including)"""
    if minVal <= value <= maxVal and round(value, 2) == value:
        return False
    return True


def is_admin() -> bool:
    """Check if jwt_token contains is_admin claim, and it is not None"""
    claims: dict = get_jwt()
    return claims and claims['is_admin']
