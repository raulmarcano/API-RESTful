from fastapi import HTTPException
from database.db import add_mortgage_simulation
from services.client_service import ClientService

class MortgageService:
    @staticmethod
    def calc_mortgage(capital: float, tae: float, years: int):
        i = tae / 100 / 12
        n = years * 12 
        monthly_pay = capital * i / (1 - (1 + i) ** -n)
        total = monthly_pay * n

        return {
            "monthly_pay": round(monthly_pay, 2),
            "total": round(total, 2)
        }
        
    @staticmethod
    def simulate_mortgage(nif: str, tae: float, years: int):
        client = ClientService.find_client(nif)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found with the given NIF")
        if tae <= 0 or years <= 0:
            raise HTTPException(status_code=422, detail="Invalid TAE or years of payment")

        simulation = MortgageService.calc_mortgage(client["capital"], tae, years)  # ✅ Ahora funciona bien
        add_mortgage_simulation(nif, client["capital"], tae, years, simulation["monthly_pay"], simulation["total"])

        return {
            "nif": nif,
            "capital": client["capital"],
            "tae": tae,
            "years": years,
            "monthly_pay": simulation["monthly_pay"],
            "total": simulation["total"]
        }
