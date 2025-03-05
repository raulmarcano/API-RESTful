import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_name="sqlite/database.db"):
        self.db_name = db_name
        self.create_clients_table()
        self.create_mortgage_simulation_table()
        
    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
        except Error as e:
            print(e)
        return conn

    def create_clients_table(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                nif TEXT NOT NULL UNIQUE,
                capital REAL NOT NULL
            );
        ''')
        conn.commit()
        conn.close()

    def create_mortgage_simulation_table(self):
        """Crea la tabla de simulaciones hipotecarias."""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mortgage_simulations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nif TEXT NOT NULL,
                capital REAL NOT NULL,
                tae REAL NOT NULL,
                years INTEGER NOT NULL,
                monthly_pay REAL NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (nif) REFERENCES clients(nif)
            );
        ''')
        conn.commit()
        conn.close()

    # Función para agregar un cliente
    def add_client(self, username: str, email: str, nif: str, capital: float):
        nif = nif.upper()
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO clients (username, email, nif, capital)
                VALUES (?, ?, ?, ?)
            ''', (username, email, nif, capital))
            conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Email or NIF already exists")
        finally:
            conn.close()

    # Función para actualizar un cliente por NIF
    def update_client(self, username: str, email: str, nif: str, capital: float):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT id FROM clients WHERE nif = ?
            ''', (nif,))
            client = cursor.fetchone()

            if client:
                cursor.execute('''
                    UPDATE clients
                    SET username = ?, email = ?, capital = ?
                    WHERE nif = ?
                ''', (username, email, capital, nif))
                conn.commit()
                return {"username": username, "email": email, "nif": nif, "capital": capital}
            else:
                raise FileNotFoundError("NIF does not exist")
        finally:
            conn.close()

    # Función para obtener un cliente por NIF
    def get_client_by_nif(self, nif: str):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT username, email, nif, capital FROM clients WHERE nif = ?
            ''', (nif,))
            client = cursor.fetchone()
            
            if client:
                username, email, nif, capital = client
                return {
                    "username": username,
                    "email": email,
                    "nif": nif,
                    "capital": capital
                }       
            else:
                raise FileNotFoundError("NIF does not exist")
        finally:
            conn.close()
            
    # Función para eliminar un cliente por NIF
    def delete_client_by_nif(self, nif: str):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            client = self.get_client_by_nif(nif)  # Se llama correctamente el método de la instancia

            if client:
                cursor.execute('''
                    DELETE FROM clients WHERE nif = ?
                ''', (nif,))
                conn.commit()
                return {"message": f"Client with NIF:{nif} successfully deleted"}
            else:
                raise FileNotFoundError("NIF does not exist")
        finally:
            conn.close()

    # Función para añadir datos de amortización a la tabla
    def add_mortgage_simulation(self, nif: str, capital: float, tae: float, years: int, monthly_pay: float, total: float):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO mortgage_simulations (nif, capital, tae, years, monthly_pay, total)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nif, capital, tae, years, monthly_pay, total))
            conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Error saving simulation in database")
        finally:
            conn.close()

db = Database()