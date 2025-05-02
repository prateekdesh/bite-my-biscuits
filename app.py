from fastapi import FastAPI, Response, Depends
from pydantic import BaseModel
from lethimcookie import bake, validate, sessions
from expiry import checkExpiry, setExpiry

username = "prateek"
password = "ilovechhavi"


class User(BaseModel):
    username: str
    password: str


app = FastAPI()

@app.post("/login")
def login(user: User, response: Response):
    if user.username == username and user.password == password:
        session_id = bake()
        sessions.append(session_id)
        expiry = setExpiry()
        print(sessions)
        response.set_cookie(key="Authorization", value=str(session_id), httponly=True)
        response.set_cookie(key="Expiry", value=str(expiry), httponly=True)
        return "Logged in"
    else:
        return "Wrong username/password"
    
@app.get("/protected")
def protected(response: Response, authorized: bool = Depends(validate), expired: bool = Depends(checkExpiry)):
    if not authorized:
        return "Protected! Login first"
    
    if expired:
        response.delete_cookie(key="Authorization")
        response.delete_cookie(key="Expiry")
        return "Cookies ded lol"
    
    return "Welcome to the protected route!"

@app.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="Authorization")
    response.delete_cookie(key="Expiry")
    return "Logged out successfully"
