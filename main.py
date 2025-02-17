
from fastapi import FastAPI, HTTPException
import uvicorn
from db import create_table, add_client
from models import ClientModel

app = FastAPI(
    title= "API_REST",
    docs_url="/docs",
    root_path="/")

# Crear la tabla de clientes si no existe
create_table()

@app.get("", summary="Basic route", description="Returns a basic message for testing a route")
def root():
    return{"message": "It´s aliveee!"}

@app.post("/add_client", summary="Add a client", description="Adds a new client")
def create_client(client: ClientModel):
    try:
        add_client(client.username, client.email, client.dni, client.capital_solicitado)
        return {"username": client.username, "email": client.email, "dni": client.dni, "capital_solicitado": client.capital_solicitado}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))