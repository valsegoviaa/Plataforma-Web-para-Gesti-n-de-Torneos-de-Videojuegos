import sqlite3

def add_column_edad():
    conn = sqlite3.connect('database/torneo.db')  # Asegúrate de que esta sea tu ruta correcta
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE usuarios ADD COLUMN edad INTEGER")
        conn.commit()
        print("Columna 'edad' añadida correctamente.")
    except sqlite3.OperationalError as e:
        print("Error:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    add_column_edad()
