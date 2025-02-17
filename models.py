from pydantic import BaseModel


class ClientModel(BaseModel):
    username: str
    dni: str
    email: str
    capital_solicitado: float