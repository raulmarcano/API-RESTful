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
            dni TEXT NOT NULL UNIQUE,  -- Campo para el DNI
            capital REAL NOT NULL  -- Campo para el capital solicitado
        );
    ''')
    conn.commit()
    conn.close()


# Función para agregar un cliente
def add_client(username: str, email: str, dni: str, capital: float):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO clients (username, email, dni, capital)
            VALUES (?, ?, ?, ?)
        ''', (username, email, dni, capital))
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception("Email or DNI already exists")
    conn.close()

# Función para actualizar un cliente por DNI
def update_client(username: str, email: str, dni: str, capital: float):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id FROM clients WHERE dni = ?
    ''', (dni,))
    client = cursor.fetchone()

    if client:
        cursor.execute('''
            UPDATE clients
            SET username = ?, email = ?, capital = ?
            WHERE dni = ?
        ''', (username, email, capital, dni))
        conn.commit()
        conn.close()
        return {"username": username, "email": email, "dni": dni, "capital": capital}
    else:
        conn.close()
        return None  # Si no encuentra el cliente, devuelve None
