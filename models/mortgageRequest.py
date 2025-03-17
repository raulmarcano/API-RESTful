from pydantic import BaseModel

class MortgageRequest(BaseModel):
    nif: str
    tae: float
    years: int
