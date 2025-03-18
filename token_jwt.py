from datetime import datetime, timedelta
from os import getenv
from jwt import encode, decode, exceptions
from fastapi.responses import JSONResponse

def expire_date(days: int):
    date = datetime.now()
    expiration_date = date + timedelta(days=days)
    return expiration_date

def write_token(data: dict):
    token = encode(
        payload={**data, "exp": expire_date(2)},
        key=getenv("SECRET"),
        algorithm="HS256"
    )
    return token

def validate_token(token):
    try:
        decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        return JSONResponse(content={"message":"Invalid Token"}, status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message":"Token Expired"}, status_code=401)