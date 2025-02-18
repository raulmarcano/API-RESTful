
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

@app.get("/", summary="Basic route", description="Returns a basic message for testing a route")
def root():
    return{"message": "It´s aliveee!"}

@app.post("/add_client", summary="Add a client",
          description="Stores client data including username, email, DNI, and requested capital.",
          response_model=ClientModel)
@handle_exceptions
async def add_client_rout(client: ClientModel):
    if not validate_nif(client.dni):
        raise HTTPException(status_code=400, detail="Invalid NIF/NIE format")
    add_client(client.username, client.email, client.dni.upper(), client.capital)
    return client

@app.post("/update_client", summary="Update a client", description="Updates client data.")
@handle_exceptions
async def update_client_rout(client: ClientModel):
    updated_client = update_client(client.username, client.email, client.dni, client.capital)
    if updated_client:
        return updated_client