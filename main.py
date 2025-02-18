
from fastapi import FastAPI, HTTPException
import uvicorn
from db import *
from models import ClientModel
from helpers import *

app = FastAPI(
    title= "API_REST",
    docs_url="/docs",
    root_path="/")

# Crear la tabla de clientes si no existe
create_table()

@app.get("/", 
         summary="Basic route", 
         description="Returns a basic message for testing a route", 
         responses={
             200: {
                 "description": "It is really alive.",
                 "content": {
                     "application/json": {
                         "example": {"message": "It's aliveee!"}
                     }
                 }
             }
         })
def root():
    return{"message": "It´s aliveee!"}

@app.post("/add_client",
          summary="Add a client",
          description="Stores client data including username, email, nif, and requested capital. It first validates email and nif",
          response_model=ClientModel,
          responses={
              400: {
                  "description": "Invalid NIF/NIE format"
              },
              422: {
                  "description": "Unprocessable Entity"
              }
          })
@handle_exceptions
async def add_client_rout(client: ClientModel):
    if not validate_nif(client.nif):
        raise HTTPException(status_code=400, detail="Invalid NIF format")
    add_client(client.username, client.email, client.nif.upper(), client.capital)
    return client

@app.post("/update_client",
          summary="Update a client",
          description="Updates client data.",
          response_model=ClientModel,
          responses={
              404: {
                  "description": "Resource not found: NIF do not exists"
              },
              422: {
                  "description": "Unprocessable Entity"
              }
          })
@handle_exceptions
async def update_client_rout(client: ClientModel):
    updated_client = update_client(client.username, client.email, client.nif, client.capital)
    if updated_client:
        return updated_client