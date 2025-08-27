import sqlite3

def add_admin():
    conn = sqlite3.connect('database/torneo.db')
    c = conn.cursor()

    email_admin = 'cami@admin.com'

    # Comprobar si ya existe el admin
    c.execute("SELECT * FROM usuarios WHERE email = ?", (email_admin,))
    if c.fetchone():
        print("El admin ya existe o el email está duplicado.")
        conn.close()
        return

    # Insertar admin
    try:
        c.execute('''
            INSERT INTO usuarios (nombre, email, contrasena, nivel, juego, rol)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Camila', email_admin, 'camipass', None, None, 'admin'))
        conn.commit()
        print("Admin creado exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear admin: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    add_admin()
