import sqlite3
import os

# Crear carpeta database si no existe
if not os.path.exists('database'):
    os.makedirs('database')

# Eliminar la base de datos existente (solo para desarrollo)
if os.path.exists('database/torneo.db'):
    os.remove('database/torneo.db')

conn = sqlite3.connect('database/torneo.db')
cursor = conn.cursor()

# Crear tabla de usuarios
cursor.execute('''
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL,
    rol TEXT DEFAULT 'participante',
    nivel TEXT
)
''')

# Crear tabla de participantes (jugadores en torneos)
cursor.execute('''
CREATE TABLE participante (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER NOT NULL,
    nivel TEXT NOT NULL,
    torneo_id INTEGER,
    puntaje INTEGER DEFAULT 0,
    FOREIGN KEY (torneo_id) REFERENCES torneo(id)
)
''')

# Crear tabla de torneos
cursor.execute('''
CREATE TABLE torneo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT
)
''')

conn.commit()
conn.close()

print("Base de datos creada correctamente con tablas: usuarios, participante y torneo.")
