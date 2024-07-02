from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import hashlib

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta'  # Clave secreta para la sesión
db = SQLAlchemy(app)

# Definición del modelo de Usuario en la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    hash_contraseña = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Creación de la base de datos y las tablas necesarias
with app.app_context():
    db.create_all()

# Lista de usuarios y contraseñas (en texto plano, para este ejemplo)
usuarios = {
    'usuario1': 'contraseña1',
    'usuario2': 'contraseña2',
    'usuario3': 'contraseña3'
}

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la página de registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre']
        contraseña = request.form['contraseña']

        # Hashear la contraseña antes de guardarla
        hash_contraseña = hashlib.sha512(contraseña.encode()).hexdigest()

        # Crear un nuevo usuario y guardarlo en la base de datos
        nuevo_usuario = Usuario(nombre=nombre_usuario, hash_contraseña=hash_contraseña)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for('login'))  # Redirigir al login después del registro

    return render_template('registro.html')

# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre']
        contraseña = request.form['contraseña']

        # Validar las credenciales
        if nombre_usuario in usuarios and usuarios[nombre_usuario] == contraseña:
            # Guardar el nombre de usuario en la sesión
            session['usuario'] = nombre_usuario
            return redirect(url_for('index'))  # Redirigir al inicio después de iniciar sesión

        # Mensaje de error si las credenciales son incorrectas
        error = "Nombre de usuario o contraseña incorrectos. Inténtelo de nuevo."
        return render_template('login.html', error=error)

    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Eliminar el nombre de usuario de la sesión
    return redirect(url_for('index'))  # Redirigir al inicio después de cerrar sesión

# Ruta para la página que muestra todos los usuarios almacenados en la base de datos
@app.route('/usuarios')
def ver_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

if __name__ == "__main__":
    app.run(port=5800, debug=True)
