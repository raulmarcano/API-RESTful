
from fastapi import FastAPI, HTTPException, Query
import uvicorn
from db import *
from models import ClientModel
from helpers import *

app = FastAPI(
    title= "API_REST",
    description="An API for managing clients and mortgage simulations.",
    docs_url="/docs",
    root_path="/api")

# Crear la tabla de clientes si no existe
create_table()
create_mortgage_simulation_table()

@app.get("/", 
         summary="Test route", 
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
                  "description": "Resource not found: NIF does not exist"
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
         summary="Get a client by NIF", 
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
async def get_client_rout(nif: str = Query(..., description="The NIF (DNI or NIE) of the client to retrieve. It should be a valid 8-12 character identifier.")):
    client = get_client_by_nif(nif)
    return client

@app.post("/simulate_mortgage",
          summary="Simulate a mortgage for a client",
          description="Calculates the monthly mortgage payment and total amount to be repaid based on the client's capital, TAE and term.",
          responses={
                200: {
                  "description": "Successful mortgage simulation",
                  "content": {
                      "application/json": {
                          "example": {
                              "nif": "55127366T",
                              "capital": 100000,
                              "tae": 3.5,
                              "years": 20,
                              "monthly_pay": 579.98,
                              "total": 139195.20
                            }
                        }
                    }
                },
              404: {
                  "description": "Client not found with the given NIF"
              },
              422: {
                  "description": "Unprocessable Entity. The provided TAE or term is invalid."
              }
          })
@handle_exceptions
async def simulate_mortgage(nif: str = Query(..., description="The NIF (DNI or NIE) of the client to retrieve. It should be a valid 8-12 character identifier."),
                            tae: float = Query(..., description="Annual Percentage Rate"), 
                            years: int = Query(..., description="Number of years over which the mortgage will be repaid")):
    client = get_client_by_nif(nif.upper())
    if not client:
        raise HTTPException(status_code=404, detail="Client not found with the given NIF")
    if tae <= 0 or years <= 0:
        raise HTTPException(status_code=422, detail="Invalid TAE or years of payment")

    simulation = calc_mortgage(client["capital"], tae, years)
    add_mortgage_simulation(nif, client["capital"], tae, years, simulation["montly_pay"], simulation["total"])

    return {
        "nif": nif,
        "capital": client["capital"],
        "tae": tae,
        "years": years,
        "monthly_pay": simulation["montly_pay"],
        "total": simulation["total"]
    }

@app.delete("/delete_client",
            summary="Delete a client and related mortgage simulations",
            description="Deletes a client and all associated mortgage simulations from the database.",
            responses={
                200: {
                    "description": "Successful deletion",
                    "content": {
                        "application/json": {
                            "example": {
                                "message": "Client and related mortgage simulations successfully deleted"
                            }
                        }
                    }
                },
                404: {
                    "description": "Client not found with the given NIF"
                },
                422: {"description": "Invalid NIF"}
            })
@handle_exceptions
async def delete_client(nif: str = Query(..., description="The NIF of the client to delete.")):
    client = get_client_by_nif(nif.upper())
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    delete_client_by_nif(nif.upper())
    return {"message": "Client and related mortgage simulations successfully deleted"}
