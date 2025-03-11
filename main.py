import uvicorn

from typing import Annotated
from fastapi import FastAPI, Query, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from models.clientModel import ClientModel
from services.client_service import ClientService
from services.mortgage_service import MortgageService
from utils.error_handler import handle_exceptions
from front import front_routes

app = FastAPI(
    title= "API_REST",
    description="An API for managing clients and mortgage simulations.",
    docs_url="/docs")

app.mount("/static", StaticFiles(directory="front/static"), name="static")
app.include_router(front_routes.router)


    #BACK ROUTES
@app.post("/users/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    if username == "admin" and password == "admin":
        return RedirectResponse(url="/users/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/test", 
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
def test():
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
    return ClientService.create_client(client)

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
    return ClientService.modify_client(client)

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
    return ClientService.find_client(nif)

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
    return MortgageService.simulate_mortgage(nif, tae, years)

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
    return ClientService.remove_client(nif)
