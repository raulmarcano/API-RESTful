from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine

from models.sqlalchemy import Client, MortgageSimulation, DB_Base

# Crear la conexión a la base de datos
engine = create_engine("sqlite:///./sqlite/database-alchemy.db")
DB_Base.metadata.create_all(engine)

# Crear la sesión
Session = sessionmaker(bind=engine)
session = Session()

class Database:
    def __init__(self):
        self.session = session
    
    def add_client(self, username: str, email: str, nif: str, capital: float):
        nif = nif.upper()
        new_client = Client(username=username, email=email, nif=nif, capital=capital)
        try:
            self.session.add(new_client)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise Exception("Email or NIF already exists")

    def update_client(self, username: str, email: str, nif: str, capital: float):
        client = self.session.query(Client).filter_by(nif=nif).first()
        if client:
            client.username = username
            client.email = email
            client.capital = capital
            self.session.commit()
            return {"username": username, "email": email, "nif": nif, "capital": capital}
        else:
            raise FileNotFoundError("NIF does not exist")

    def get_client_by_nif(self, nif: str):
        client = self.session.query(Client).filter_by(nif=nif).first()
        if client:
            return {"username": client.username, 
                    "email": client.email, 
                    "nif": client.nif, 
                    "capital": client.capital}
        else:
            raise FileNotFoundError("NIF does not exist")

    def delete_client_by_nif(self, nif: str):
        client = self.session.query(Client).filter_by(nif=nif).first()
        if client:
            self.session.delete(client)
            self.session.commit()
            return {"message": f"Client with NIF:{nif} successfully deleted"}
        else:
            raise FileNotFoundError("NIF does not exist")

    def add_mortgage_simulation(self, nif: str, capital: float, tae: float, years: int, monthly_pay: float, total: float):
        new_simulation = MortgageSimulation(nif=nif, 
                                            capital=capital, 
                                            tae=tae, 
                                            years=years, monthly_pay=monthly_pay, 
                                            total=total)
        try:
            self.session.add(new_simulation)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise Exception("Error saving simulation in database")

# Instancia de la base de datos
db = Database()
