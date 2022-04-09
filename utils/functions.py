from flask_jwt_extended import get_jwt
from psycopg2._psycopg import Boolean

ERROR_ACCESS_DENIED = {"message": "Error! Access denied!"}


def isfloatold(num: str) -> bool:
    """Takes a string, representing number (positive  or negative or zero), returns True is it is valid number and
    False  in other cases """
    try:
        return not num == "nan" and not num == "infinity" and type(float(num)) == float
    except:
        return False


def isfloat(num: str) -> bool:
    """Takes a string, representing number (positive  or negative or zero), returns True is it is valid number and
    False  in other cases [THIS FUNCTION FASTER FOR ABOUT 3-5%]"""
    return num.replace(".", "", 1).replace("-", "", 1).isnumeric()


def getfloat(num: str) -> float:
    """Takes a string, representing number (positive  or negative or zero), returns it float value or None"""
    try:
        return float(num)
    except ValueError:
        return None


def checkvalueinrange(value: float, minVal: float, maxVal: float) -> bool:
    """Takes value, minVal, maxVal floats and check if value in range from minVal(including) to maxVal(including)"""
    if minVal <= value <= maxVal and round(value, 2) == value:
        return True
    return False


def is_admin() -> bool:
    """Check if jwt_token contains is_admin claim, and it is not None"""
    claims = get_jwt()
    return claims and claims['is_admin']
