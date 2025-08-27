from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from functools import wraps
from database import obtener_participantes_con_resultados


app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

def db_connection():
    conn = sqlite3.connect('database/torneo.db')
    conn.row_factory = sqlite3.Row
    return conn

# Decorador para rutas que requieren login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder a esta página.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para rutas que requieren admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            flash('Acceso no autorizado. Inicia sesión como administrador.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']       # o 'username' si usas username
        password = request.form['contrasena']  # o 'password'

        conn = db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE email = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and password == user['contrasena']:
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            session['user_role'] = user['rol']

            # Redirigir según el rol
            if user['rol'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos')

    return render_template('login.html')

# Dashboard admin
@app.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    # Esto también podrías hacerlo sin el decorador, chequeando la sesión aquí
    # if not session.get('user_id') or session.get('user_role') != 'admin':
    #     return redirect(url_for('login'))

    conn = db_connection()
    c = conn.cursor()
    c.execute("SELECT nombre, email, nivel FROM usuarios WHERE rol = 'participante'")
    participantes = c.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', participantes=participantes)


# Dashboard participante
@app.route('/participant_dashboard')
@login_required
def participant_dashboard():
    if session.get('user_role') != 'participante':
        flash('Acceso denegado: solo participantes', 'danger')
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    conn = db_connection()
    c = conn.cursor()

    c.execute("SELECT nombre, nivel FROM usuarios WHERE id = ?", (user_id,))
    participante = c.fetchone()
    conn.close()

    return render_template('participant_dashboard.html', participante=participante)
# Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        email = request.form.get('email', '').strip()
        contrasena = request.form.get('contrasena', '').strip()
        nivel = request.form.get('nivel', '').strip()
        edad = request.form.get('edad', '').strip()
        juego = "LOL"         # valor fijo, no desde el formulario
        torneo = "LOL World"  # valor fijo, no desde el formulario

        if not usuario or not email or not contrasena or not nivel or not edad:
            error = "Por favor, rellena todos los campos."
            return render_template('register.html', error=error)

        conn = db_connection()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO usuarios (nombre, email, contrasena, rol, nivel, edad, juego, torneo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (usuario, email, contrasena, 'participante', nivel, edad, juego, torneo)
            )
            conn.commit()
            flash('Registro exitoso, ahora puedes iniciar sesión', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            error = 'Este correo ya está registrado.'
            return render_template('register.html', error=error)
        finally:
            conn.close()

    return render_template('register.html')

# Listar participantes - ejemplo para admin
@app.route('/manage_participants')
@admin_required
def manage_participants():
    conn = db_connection()
    c = conn.cursor()

    # Consulta que incluye la nueva columna 'juego'
    c.execute("SELECT id, nombre, email, juego, nivel FROM usuarios WHERE rol = 'participante'")

    participantes = c.fetchall()
    conn.close()

    return render_template('manage_participants.html', participantes=participantes)# Agregar participante (como usuario admin)

@app.route('/add_participant', methods=['GET', 'POST'])
@login_required
def add_participant():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['email']
        edad = request.form['edad']
        nivel = request.form['nivel']

        try:
            edad = int(edad)
        except ValueError:
            edad = None

        conn = db_connection()
        c = conn.cursor()
        try:
            # Juego fijo "MiTorneo" y contraseña por defecto sin hash
            c.execute(
                "INSERT INTO usuarios (nombre, email, edad, nivel, juego, contrasena, rol) VALUES (?, ?, ?, ?, ?, ?, 'participante')",
                (nombre, correo, edad, nivel, 'LOL', 'default123')
            )
            conn.commit()
            flash('Participante agregado correctamente', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError as e:
            flash(f'Error al agregar participante: {e}', 'error')
        finally:
            conn.close()

    return render_template('add_participant.html')

# Editar participante
@app.route('/edit_participant/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_participant(id):
    conn = db_connection()
    c = conn.cursor()

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        nivel = request.form.get('nivel', '').strip()

        if not nombre or not nivel:
            error = "Todos los campos son obligatorios."
            return render_template('edit_participant.html', error=error)

        c.execute("UPDATE usuarios SET nombre = ?, nivel = ? WHERE id = ?", (nombre, nivel, id))
        conn.commit()
        conn.close()
        flash('Participante actualizado correctamente.', 'success')
        return redirect(url_for('index'))

    c.execute("SELECT * FROM usuarios WHERE id = ? AND rol = 'participante'", (id,))
    participante = c.fetchone()
    conn.close()

    if participante:
        return render_template('edit_participant.html', participante=participante)
    else:
        flash('Participante no encontrado.', 'danger')
        return redirect(url_for('manage_participants'))

# Eliminar participante
@app.route('/delete_participant/<int:id>')
@admin_required
def delete_participant(id):
    conn = db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM usuarios WHERE id = ? AND rol = 'participante'", (id,))
    conn.commit()
    conn.close()
    flash('Participante eliminado.', 'success')
    return redirect(url_for('index'))

@app.route('/estadisticas')
def estadisticas():
    conn = db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('''
        SELECT nombre, victorias, empates, derrotas, puntaje
        FROM usuarios
        WHERE rol = 'participante'
        ORDER BY puntaje DESC
    ''')
    participantes = c.fetchall()
    conn.close()

    return render_template('estadisticas.html', participantes=participantes)

# Ruta principal
@app.route('/')
def index():
    conn = db_connection()
    c = conn.cursor()
    filtro = request.args.get('buscar', '').strip()

    if filtro:
        filtro_like = f"%{filtro}%"
        c.execute(
            '''SELECT id, nombre, nivel, edad, juego FROM usuarios 
               WHERE rol = 'participante' AND LOWER(nombre) LIKE LOWER(?)''',
            (filtro_like,))
    else:
        c.execute("SELECT id, nombre, nivel, edad, juego FROM usuarios WHERE rol = 'participante'")

    participantes = c.fetchall()
    conn.close()

    torneo_nombre = "LOL World"

    return render_template('index.html', participantes=participantes, torneo=torneo_nombre)

@app.route('/asignar_puntajes', methods=['GET', 'POST'])
def asignar_puntajes():
    conn = db_connection()
    c = conn.cursor()

    if request.method == 'POST':
        c.execute("SELECT id FROM usuarios WHERE rol = 'participante'")
        participantes = c.fetchall()

        for p in participantes:
            id = p[0]
            victorias = int(request.form.get(f'victorias_{id}', 0))
            empates = int(request.form.get(f'empates_{id}', 0))
            derrotas = int(request.form.get(f'derrotas_{id}', 0))
            puntaje = victorias * 3 + empates

            c.execute('''
                UPDATE usuarios
                SET victorias = ?, empates = ?, derrotas = ?, puntaje = ?
                WHERE id = ?
            ''', (victorias, empates, derrotas, puntaje, id))

        conn.commit()
        flash('Puntajes actualizados correctamente', 'success')
        return redirect(url_for('asignar_puntajes'))

    c.execute("SELECT id, nombre, victorias, empates, derrotas, puntaje FROM usuarios WHERE rol = 'participante' ORDER BY puntaje DESC")
    participantes = c.fetchall()
    conn.close()

    return render_template('asignar_puntajes.html', participantes=participantes)

@app.route('/grafica')
def grafica():
    participantes = obtener_participantes_con_resultados()
    total_ganadas = sum(p.get('victorias', 0) for p in participantes)
    total_empatadas = sum(p.get('empates', 0) for p in participantes)
    total_perdidas = sum(p.get('derrotas', 0) for p in participantes)

    return render_template('grafica.html',
                           ganadas=total_ganadas,
                           empatadas=total_empatadas,
                           perdidas=total_perdidas)

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
