from typing import Union

from flask_jwt_extended import get_jwt
import hmac

ERROR_ACCESS_DENIED = {"message": "Error! Access denied!"}

PERIOD_TYPES = ["hour", "day", "week", "month"]


def safe_str_cmp(a: str, b: str) -> bool:
    """This function compares strings in somewhat constant time. This
    requires that the length of at least one string is known in advance.

    Returns `True` if the two strings are equal, or `False` if they are not.
    """

    if isinstance(a, str):
        a = a.encode("utf-8")  # type: ignore

    if isinstance(b, str):
        b = b.encode("utf-8")  # type: ignore

    return hmac.compare_digest(a, b)


def isfloat(num: str) -> bool:
    """Takes a string, representing number (positive  or negative or zero), returns True is it is valid number and
    False  in other cases [THIS FUNCTION FASTER FOR ABOUT 3-5%]"""
    return num.replace(".", "", 1).replace("-", "", 1).isnumeric()


def getfloat(num: str) -> Union[float, None]:
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
