from flask_jwt_extended import get_jwt

ERROR_ACCESS_DENIED = {"message": "Error! Access denied!"}


def isfloat(num: str):
    try:
        return not num == "nan" and not num == "infinity" and type(float(num)) == float
    except:
        return False


def getfloat(num):
    try:
        return float(num)
    except ValueError:
        return None


def checkrange(value, minVal, maxVal):
    if minVal <= value <= maxVal and round(value, 2) == value:
        return True
    return False


def is_admin():
    claims = get_jwt()
    return claims['is_admin']
