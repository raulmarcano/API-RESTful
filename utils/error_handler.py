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

