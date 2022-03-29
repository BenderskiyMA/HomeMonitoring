
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
