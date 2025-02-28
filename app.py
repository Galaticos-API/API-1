from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/atestados/')
def atestado():
    return render_template('atestados.html')

@app.route('/avaliacao/')
def avaliacao():
    return render_template('avaliacao.html')

@app.route('/login/')
def login():
    return render_template('/user/login.html')

@app.route('/cadastro/')
def cadastro():
    return render_template('/user/cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
