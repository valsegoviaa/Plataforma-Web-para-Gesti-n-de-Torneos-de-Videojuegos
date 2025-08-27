import sqlite3

def add_torneo_column():
    conn = sqlite3.connect('database/torneo.db')  # Cambia por la ruta correcta
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE usuarios ADD COLUMN torneo TEXT DEFAULT 'LOL World'")
        print("Columna 'torneo' añadida correctamente.")
    except sqlite3.OperationalError as e:
        print("Error al añadir columna 'torneo':", e)
    finally:
        conn.commit()
        conn.close()

if __name__ == '__main__':
    add_torneo_column()
