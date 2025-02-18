
from fastapi import FastAPI, HTTPException, Query
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
    updated_client = update_client(client.username, client.email, client.nif.upper(), client.capital)
    if updated_client:
        return updated_client

  
@app.get("/get_client", 
         summary="Get a client by DNI", 
         description="Returns client data by providing their NIF.",
         response_model=ClientModel,
         responses={
             404: {
                 "description": "Client not found with the given NIF"
             },
             422: {
                 "description": "Unprocessable Entity. The provided NIF is invalid or does not match the expected format."
             }
         })
@handle_exceptions
async def get_client(nif: str = Query(..., description="The NIF (DNI or NIE) of the client to retrieve. It should be a valid 8-12 character identifier.")):
    client = get_client_by_nif(nif)
    return client