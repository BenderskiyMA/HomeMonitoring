from flask_jwt_extended import get_jwt


ERROR_ACCESS_DENIED = {"message": "Error! Access denied!"}

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
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
