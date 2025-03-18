import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from front import front_routes
from routes import back_routes
from routes.auth import auth_routes

app = FastAPI(
    title= "API_REST",
    description="An API for managing clients and mortgage simulations.",
    docs_url="/docs")

app.mount("/static", StaticFiles(directory="front/static"), name="static")
app.include_router(front_routes.router)
app.include_router(back_routes.router)

app.include_router(auth_routes, prefix="/api")
load_dotenv()