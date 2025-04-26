from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Base de datos simulada con roles y contraseñas hasheadas
usuarios = {
    'admin': {'password': generate_password_hash('12345'), 'role': 'admin'},
    'johndoe': {'password': generate_password_hash('secreto'), 'role': 'user'}
}

# Clase de Usuario
class Usuario(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = usuarios[username]['role']

# Cargar usuario desde la sesión
@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return Usuario(user_id)
    return None

# Ruta principal protegida
@app.route('/')
@login_required
def home():
    return render_template('home.html.jinja2', nombre=current_user.id, role=current_user.role)

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validar si los datos enviados existen en la lista 'usuarios'
        if username in usuarios and check_password_hash(usuarios[username]['password'], password):
            user = Usuario(username)
            login_user(user)
            return redirect(url_for('home'))  # Redirigir a la página 'home.html'
        
        return render_template("error.html.jinja2", error_code=401, 
                               error_message="Invalid Credentials (error on username or password)!"), 401
    
    # Página llamada sino se envían datos, método GET
    return render_template('login.html.jinja2')

# Ruta de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
