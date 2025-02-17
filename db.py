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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            dni TEXT NOT NULL UNIQUE,  -- Campo para el DNI
            capital_solicitado REAL NOT NULL  -- Campo para el capital solicitado
        );
    ''')
    conn.commit()
    conn.close()


# Función para agregar un cliente
def add_client(username: str, email: str, dni: str, capital_solicitado: float):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO clients (username, email, dni, capital_solicitado)
            VALUES (?, ?, ?, ?)
        ''', (username, email, dni, capital_solicitado))
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception("Email or DNI already exists")
    conn.close()
