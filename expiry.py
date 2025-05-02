import datetime
import time
from fastapi import Request

def getCurrent():
    date_time = datetime.datetime.now()
    current = time.mktime(date_time.timetuple())
    expiry = current+86400

    return current, expiry



def setExpiry() -> str:
    exp = getCurrent()[1]
    return exp

def checkExpiry(request: Request) -> bool:
    current = getCurrent()[0]
    expiry = request.cookies.get("Expiry")
    if not expiry:
        return True
    if float(current) > float(expiry):
        return True
    return False