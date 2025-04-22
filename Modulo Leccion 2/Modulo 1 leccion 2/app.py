from flask import Flask, request, jsonify

app = Flask(__name__)

todos = {"todos": ["Estudiar","Comer","Jugar"] }

@app.route("/", methods=["GET"])
def home():
    return "Simple TODO API"

@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def insert_todo():
    data = request.json
    if not data or "todo" not in data:
        return jsonify({"error": "Datos incompl"}), 400
    
    todos["todos"].append(data['todo'])

    return jsonify(todos)

if __name__ == "__main__":
    app.run(debug=True)