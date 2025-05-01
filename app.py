from fastapi import FastAPI, Response, Depends
from pydantic import BaseModel
from lethimcookie import bake, validate, sessions

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
        print(sessions)
        response.set_cookie(key="Authorization", value=str(session_id), httponly=True)
        return "Logged in"
    else:
        return "Nikal Lawde"
    
@app.get("/protected")
def protected(authorized: bool = Depends(validate)):
    if not authorized:
        return "protected! Login first"
    
    return "Welcome to the protected route!"

@app.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="Authorization")
    return "Logged out successfully"
