from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

DB_Base = declarative_base()

# Definición de modelos
class Client(DB_Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    nif = Column(String(12), unique=True, nullable=False)
    capital = Column(Float, nullable=False)

    # Relación con la simulación hipotecaria
    simulations = relationship("MortgageSimulation", back_populates="client")

class MortgageSimulation(DB_Base):
    __tablename__ = 'mortgage_simulations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nif = Column(String(12), ForeignKey('clients.nif'), nullable=False)
    capital = Column(Float, nullable=False)
    tae = Column(Float, nullable=False)
    years = Column(Integer, nullable=False)
    monthly_pay = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    # Relación con el cliente
    client = relationship("Client", back_populates="simulations")

# Crear la conexión a la base de datos
engine = create_engine("sqlite:///./sqlite/database-alchemy.db")

DB_Base.metadata.create_all(engine)
