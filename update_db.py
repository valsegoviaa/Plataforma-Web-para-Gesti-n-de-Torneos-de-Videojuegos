import sqlite3

DB_PATH = 'database/torneo.db'  # Ajusta la ruta correcta

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Verificar si la columna 'edad' ya existe
cursor.execute("PRAGMA table_info(participante);")
columns = [col[1] for col in cursor.fetchall()]

if 'edad' not in columns:
    try:
        cursor.execute("ALTER TABLE participante ADD COLUMN edad INTEGER;")
        print("Columna 'edad' añadida con éxito.")
    except sqlite3.OperationalError as e:
        print("Error al añadir la columna 'edad':", e)
else:
    print("La columna 'edad' ya existe en la tabla participante.")

conn.commit()
conn.close()
