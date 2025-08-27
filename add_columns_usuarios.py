import sqlite3

def agregar_columnas_usuarios():
    conn = sqlite3.connect('database/torneo.db')
    c = conn.cursor()

    try:
        c.execute("ALTER TABLE usuarios ADD COLUMN victorias INTEGER DEFAULT 0")
        print("Columna 'victorias' añadida")
    except sqlite3.OperationalError:
        print("La columna 'victorias' ya existe")

    try:
        c.execute("ALTER TABLE usuarios ADD COLUMN empates INTEGER DEFAULT 0")
        print("Columna 'empates' añadida")
    except sqlite3.OperationalError:
        print("La columna 'empates' ya existe")

    try:
        c.execute("ALTER TABLE usuarios ADD COLUMN derrotas INTEGER DEFAULT 0")
        print("Columna 'derrotas' añadida")
    except sqlite3.OperationalError:
        print("La columna 'derrotas' ya existe")

    try:
        c.execute("ALTER TABLE usuarios ADD COLUMN puntaje INTEGER DEFAULT 0")
        print("Columna 'puntaje' añadida")
    except sqlite3.OperationalError:
        print("La columna 'puntaje' ya existe")

    conn.commit()
    conn.close()

agregar_columnas_usuarios()
