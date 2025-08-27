import sqlite3

DB_PATH = 'database/torneo.db'

def get_participantes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT participante.id, participante.nombre, participante.edad, participante.nivel, torneo.nombre AS torneo
        FROM participante
        LEFT JOIN torneo ON participante.torneo_id = torneo.id
    ''')
    participantes = cursor.fetchall()
    conn.close()
    return participantes

def get_torneos():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM torneo")
    torneos = cursor.fetchall()
    conn.close()
    return torneos

def add_torneo(nombre_torneo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO torneo (nombre) VALUES (?)", (nombre_torneo,))
    conn.commit()
    conn.close()
    print(f"Torneo '{nombre_torneo}' agregado exitosamente.")

def obtener_participantes():
    conn = sqlite3.connect('database/torneo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ganadas, empatadas, perdidas FROM participante")
    rows = cursor.fetchall()
    conn.close()

    participante = []
    for row in rows:
        participante.append({
            'ganadas': row[0],
            'empatadas': row[1],
            'perdidas': row[2]
        })
    return participante

import sqlite3

def obtener_participantes_con_resultados():
    conn = sqlite3.connect('database/torneo.db')  # Asegúrate de que la ruta es correcta
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nombre, victorias, empates, derrotas, puntaje
        FROM usuarios
        WHERE rol = 'participante'
        ORDER BY puntaje DESC
    """)

    participantes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return participantes

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabla de usuarios (sin juego, con nivel)
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            nivel TEXT,
            rol TEXT DEFAULT 'participante'
        )
    ''')

    # Tabla de torneos
    c.execute('''
        CREATE TABLE IF NOT EXISTS torneo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
    ''')

    # Tabla de participantes sin juego ni equipo
    c.execute('''
        CREATE TABLE IF NOT EXISTS participante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            nivel TEXT,
            torneo_id INTEGER,
            puntaje INTEGER DEFAULT 0,
            FOREIGN KEY (torneo_id) REFERENCES torneo (id)
        )
    ''')

    conn.commit()
    conn.close()

init_db()
