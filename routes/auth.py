from fastapi import APIRouter, Header
from pydantic import BaseModel, EmailStr
from token_jwt import validate_token, write_token
from fastapi.responses import JSONResponse

auth_routes= APIRouter()

class User(BaseModel):
    username:str
    email: EmailStr

@auth_routes.post("/auth")
def login(user: User):
    print(user)
    if user.username == "admin":
        return write_token(user.model_dump())
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)


@auth_routes.post("/verify/token")
def verify_token(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    return validate_token(token)