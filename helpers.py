from fastapi import HTTPException

def handle_exceptions(func):
    """Función de manejo de errores reutilizable para las rutas"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as ve:
            raise HTTPException(status_code=422, detail=f"Validation error: {str(ve)}")
        except ConnectionError as ce:
            raise HTTPException(status_code=503, detail=f"Database connection error: {str(ce)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return wrapper
