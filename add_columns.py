import sqlite3

conn = sqlite3.connect('database/torneo.db')
c = conn.cursor()

try:
    c.execute("ALTER TABLE participante ADD COLUMN victorias INTEGER DEFAULT 0")
except:
    print("La columna 'victorias' ya existe")

try:
    c.execute("ALTER TABLE participante ADD COLUMN empates INTEGER DEFAULT 0")
except:
    print("La columna 'empates' ya existe")

try:
    c.execute("ALTER TABLE participante ADD COLUMN derrotas INTEGER DEFAULT 0")
except:
    print("La columna 'derrotas' ya existe")

conn.commit()
conn.close()
print("Columnas añadidas correctamente (si no existían)")
