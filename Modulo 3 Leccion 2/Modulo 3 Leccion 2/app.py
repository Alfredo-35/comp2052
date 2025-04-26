from flask import Flask, jsonify, request, abort
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, AnonymousIdentity

app = Flask(__name__)
app.secret_key = 'mi_secreto'

# Configurar Flask-Principal
principals = Principal(app)

# Definir roles
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

# Simular "identidad" (en una app real sería con login)
current_user_role = 'user'  # Cambia a 'admin' para simular administrador

@app.before_request
def set_identity():
    identity = Identity('user')
    if current_user_role:
        identity.provides.add(RoleNeed(current_user_role))
    identity_changed.send(app, identity=identity)

# Rutas protegidas
@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin():
    return jsonify({"message": "Bienvenido, Admin!"})

@app.route('/user')
@user_permission.require(http_exception=403)
def user():
    return jsonify({"message": "Bienvenido, Usuario!"})

@app.errorhandler(403)
def forbidden(e):
    return jsonify({"error": "Acceso Denegado"}), 403

@app.route('/')
def index():
    return jsonify({"message": "Ruta pública"})

if __name__ == '__main__':
    app.run(debug=True)
