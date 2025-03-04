from fastapi import HTTPException
from database.db import *
from models.clientModel import ClientModel

class ClientService:
    @staticmethod
    def validate_nif(nif: str):
        nif = nif.upper()
        
        letter_dict = "TRWAGMYFPDXBNJZSQVHLCKE"
        last_letter = nif[-1]

        if nif[0] in "XYZ":  # Verificamos si es un NIE
            first_nie_dict = {'X': '0', 'Y': '1', 'Z': '2'}  # Reemplazamos la letra inicial por su número correspondiente
            nif_num = first_nie_dict[nif[0]] + nif[1:-1]
        elif nif[0].isdigit():
            nif_num = nif[0:-1]  # Tomamos todo excepto la última letra
        else:
            return False
        
        if not nif_num.isdigit():
            return False
        
        nif_integer = int(nif_num)
        letter_calc = letter_dict[nif_integer % 23]

        return last_letter == letter_calc
    
    @staticmethod
    def create_client(client: ClientModel):
        if not ClientService.validate_nif(client.nif):
            raise HTTPException(status_code=400, detail="Invalid NIF format")
        add_client(client.username, client.email, client.nif.upper(), client.capital)
        return client

    @staticmethod
    def modify_client(client: ClientModel):
        updated_client = update_client(client.username, client.email, client.nif.upper(), client.capital)
        if updated_client:
            return updated_client
        raise HTTPException(status_code=404, detail="Client not found")

    @staticmethod
    def find_client(nif: str):
        client = get_client_by_nif(nif.upper())
        if not client:
            raise HTTPException(status_code=404, detail="Client not found with the given NIF")
        return client

    @staticmethod
    def remove_client(nif: str):
        client = get_client_by_nif(nif.upper())
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        delete_client_by_nif(nif.upper())
        return {"message": "Client and related mortgage simulations successfully deleted"}

    
