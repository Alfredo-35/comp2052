from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Pagina.html')  # Página de inicio

@app.route('/')
def Accessories():
    return render_template('Accessories.html')  # Página 2

@app.route('/')
def BodyParts():
    return render_template('BodyParts.html')  # Página 3

@app.route('/')
def Mecanica():
    return render_template('Mecanica.html')  # Página 4

if __name__ == '__main__':
    app.run(debug=True)
