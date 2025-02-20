from fastapi import HTTPException
from functools import wraps

def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as http_exc:
            raise http_exc
        except ConnectionError as ce:
            raise HTTPException(status_code=503, detail=f"Database connection error: {str(ce)}")
        except FileNotFoundError as fnf:
            raise HTTPException(status_code=404, detail=f"Resource not found: {str(fnf)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return wrapper

def validate_nif(nif):
    nif = nif.upper()
    
    letter_dict = "TRWAGMYFPDXBNJZSQVHLCKE"
    last_letter = nif[-1]

    if nif[0] in "XYZ": #Verificamos si es un NIE
        first_nie_dict = {'X': '0', 'Y': '1', 'Z': '2'}  #Reemplazamos la letra inicial por su número correspondiente
        nif_num = first_nie_dict[nif[0]] + nif[1:-1]
    elif nif[0].isdigit():
        nif_num = nif[0:-1]  #Tomamos todo excepto la última letra
    else:
        return False
    
    if not nif_num.isdigit():
        return False
    
    nif_integer = int(nif_num)
    letter_calc = letter_dict[nif_integer % 23]

    return last_letter == letter_calc

def calc_mortgage(capital: float, tae: float, years: int):
    i = tae / 100 / 12
    n = years * 12 
    montly_pay = capital * i / (1 - (1 + i) ** -n)
    total = montly_pay * n

    return {
        "montly_pay": round(montly_pay, 2),
        "total": round(total, 2)
    }