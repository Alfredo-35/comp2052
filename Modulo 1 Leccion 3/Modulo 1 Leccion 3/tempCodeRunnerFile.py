from flask import Flask, request, jsonify

app = Flask(__name__)

# Datos en memoria
usuarios = []
productos = []

# Ruta: GET /info
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "nombre_sistema": "Gestor de Usuarios y Productos",
        "version": "1.0",
        "autor": "Tu Nombre"
    })

# Ruta: POST /crear_usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')

    if not nombre or not correo:
        return jsonify({"error": "Nombre y correo son obligatorios"}), 400

    usuario = {"nombre": nombre, "correo": correo}
    usuarios.append(usuario)
    return jsonify({"mensaje": "Usuario creado exitosamente", "usuario": usuario}), 201

# Ruta: GET /usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify({"usuarios": usuarios})

# Error 404 personalizado
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
