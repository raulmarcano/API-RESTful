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
        conn.close()
        return {"username": username, "email": email, "nif": nif, "capital": capital}
    else:
        conn.close()
        raise FileNotFoundError("NIF do not exists")  # Si no encuentra el cliente
