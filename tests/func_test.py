import datetime
from datetime import datetime
from random import random

from utils.functions import isfloat, isfloatold


def printtestresults(count: int, timeStart: datetime, timeStop: datetime):
    print(str(count))
    print(str(timeStart))
    print(str(timeStop))
    print(str(timeStop - timeStart))


def run_checks_old(count: int) -> str:
    timestart = datetime.now()
    i = 0
    while i < count:
        b = int(random() * 1000) / 100
        fr = "-" + str(b)
        a = 0
        if isfloatold(fr):
            a += 1
        i += 1
    timestop = datetime.now()
    printtestresults(count, timestart, timestop)


def run_checks(count: int) -> str:
    timestart = datetime.now()
    i = 0
    while i < count:
        b = int(random() * 1000) / 100
        fr = "-" + str(b)
        a = 0
        if isfloat(fr):
            a += 1
        i += 1
    timestop = datetime.now()
    printtestresults(count, timestart, timestop)


run_checks_old(1000000)
run_checks(1000000)
