from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

Jinja2_template = Jinja2Templates(directory="front/templates")


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return Jinja2_template.TemplateResponse("login.html", {"request": request})

@router.get("/users/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return Jinja2_template.TemplateResponse("dashboard.html", {"request": request})

@router.get("/add_client_form", response_class=HTMLResponse)
def add_client_form(request: Request):
    return Jinja2_template.TemplateResponse("add_client.html", {"request": request})

@router.get("/update_client_form", response_class=HTMLResponse)
def update_client_form(request: Request):
    return Jinja2_template.TemplateResponse("update_client.html", {"request": request})

@router.get("/delete_client_form", response_class=HTMLResponse)
def delete_client_form(request: Request):
    return Jinja2_template.TemplateResponse("delete_client.html", {"request": request})

@router.get("/simulate_mortgage_form", response_class=HTMLResponse)
def simulate_mortgage_form(request: Request):
    return Jinja2_template.TemplateResponse("simulate_mortgage.html", {"request": request})

@router.get("/get_client_form", response_class=HTMLResponse)
def get_client_form(request: Request):
    return Jinja2_template.TemplateResponse("get_client.html", {"request": request})
