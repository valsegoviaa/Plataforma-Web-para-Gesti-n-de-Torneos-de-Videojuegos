import sqlite3

def mostrar_columnas_usuarios():
    conn = sqlite3.connect('database/torneo.db')  # Cambia aquí por la ruta correcta
    c = conn.cursor()
    c.execute("PRAGMA table_info(usuarios);")
    columnas = c.fetchall()
    print("Columnas en la tabla usuarios:")
    for columna in columnas:
        # Cada columna es una tupla: (cid, name, type, notnull, dflt_value, pk)
        print(f" - {columna[1]} ({columna[2]})")
    conn.close()

mostrar_columnas_usuarios()
