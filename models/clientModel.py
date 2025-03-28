from pydantic import BaseModel, Field, EmailStr

class ClientModel(BaseModel):
    username: str = Field(..., title="Username", description="Full name of the client", max_length=50)
    email: EmailStr = Field(..., title="Email", description="Unique email address of the client")
    nif: str = Field(..., title="NIF", description="Unique National identifier (DNI or NIE) of the client", min_length=8, max_length=12)
    capital: float = Field(..., title="Requested Capital", description="Amount of money requested by the client", gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "Joaquin Phoenix",
                "email": "Phoenix@example.com",
                "nif": "12345678A",
                "capital": 150000
            }
        }
