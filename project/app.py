from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta'  
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    hash_contraseña = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre']
        contraseña = request.form['contraseña']
        confirmar_contraseña = request.form['confirmar_contraseña']

       
        if contraseña != confirmar_contraseña:
            flash("Las contraseñas no coinciden. Inténtelo de nuevo.")
            return redirect(url_for('registro'))

        
        usuario_existente = Usuario.query.filter_by(nombre=nombre_usuario).first()
        if usuario_existente:
            flash("El nombre de usuario ya está en uso. Intente con otro.")
            return redirect(url_for('registro'))

        
        hash_contraseña = hashlib.sha512(contraseña.encode()).hexdigest()


        nuevo_usuario = Usuario(nombre=nombre_usuario, hash_contraseña=hash_contraseña)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado exitosamente. Ahora puede iniciar sesión.")
        return redirect(url_for('login'))  

    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre']
        contraseña = request.form['contraseña']

        
        hash_contraseña = hashlib.sha512(contraseña.encode()).hexdigest()

        
        usuario = Usuario.query.filter_by(nombre=nombre_usuario, hash_contraseña=hash_contraseña).first()
        if usuario:
            session['usuario'] = nombre_usuario
            return redirect(url_for('index'))  

        flash("Nombre de usuario o contraseña incorrectos. Inténtelo de nuevo.")
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('usuario', None)  
    return redirect(url_for('index'))  

def ver_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

if __name__ == "__main__":
    app.run(port=5800, debug=True)
