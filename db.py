import sqlite3
from sqlite3 import Error

DATABASE_URL = "clients.db"

# Crear la conexión a la base de datos
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_URL)
    except Error as e:
        print(e)
    return conn

# Función para crear la tabla de clientes si no existe
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    #cursor.execute("DROP TABLE IF EXISTS clients;")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            nif TEXT NOT NULL UNIQUE,
            capital REAL NOT NULL  -- Campo para el capital solicitado
        );
    ''')
    conn.commit()
    conn.close()

# Función para agregar un cliente
def add_client(username: str, email: str, nif: str, capital: float):
    nif = nif.upper()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO clients (username, email, nif, capital)
            VALUES (?, ?, ?, ?)
        ''', (username, email, nif, capital))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        conn.close()
        raise Exception("Email or NIF already exists")

# Función para actualizar un cliente por nif
def update_client(username: str, email: str, nif: str, capital: float):
    conn = create_connection()
    try:
        cursor = conn.cursor()

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

# Función para obtener un cliente por nif
def get_client_by_nif(nif: str):
    conn = create_connection()
    try:
        cursor = conn.cursor()
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

# Función para crear la tabla de amortizaciones
def create_mortgage_simulation_table():
    conn = create_connection()
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

# Función para añadir datos de amortización a la tabla
def add_mortgage_simulation(nif: str, capital: float, tae: float, years: int, monthly_pay: float, total: float):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO mortgage_simulations (nif, capital, tae, years, monthly_pay, total)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nif, capital, tae, years, monthly_pay, total))
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception("Error saving simulation on database")
    finally:
        conn.close()
