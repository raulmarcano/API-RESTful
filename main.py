
from fastapi import FastAPI, HTTPException
import uvicorn
from db import *
from models import ClientModel
from helpers import handle_exceptions

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
async def add_client(client: ClientModel):
    add_client(client.username, client.email, client.dni, client.capital)
    return {"username": client.username, "email": client.email, "dni": client.dni, "capital_solicitado": client.capital}