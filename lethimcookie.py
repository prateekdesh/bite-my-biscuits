import secrets
from fastapi import Request

global sessions
sessions = []

def bake() -> str:
    return secrets.token_urlsafe(32)

def validate(request: Request) -> bool:
    cookie = request.cookies.get("Authorization")
    if cookie is None:
        return False
    if str(cookie) in sessions:
        return True
    return False