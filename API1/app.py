from flask import Flask, jsonify, session, redirect, url_for, render_template, request, flash
import secrets
import bcrypt
import mysql.connector

from back.user import usuarios_bp
from back.atestados import atestados_bp
from back.equipe import equipes_bp

from dotenv import load_dotenv
import os
load_dotenv()
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

def carregar_usuarios():  # Função para carregar os usuários cadastrados do MySQL
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ra, nome, senha FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios

def verifyLogin(route):
    if session.get("RA"):  # verifica se o user está logado
        return render_template(route)  # se tiver, envia para a rota especificada
    else:
        return redirect(url_for("login"))  # se nao estiver logado, vai para pagina de login

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))
    
@app.route('/')  # isso define uma rota
def home():  # funcao que é executada quando está na rota
    return verifyLogin("index.html")  #envia o caminho do arquivo para a função verifyLogin
    
@app.route('/atestados/')
def atestado():
    return verifyLogin("atestados.html")

@app.route('/equipe/')
def avaliacao():
    return verifyLogin("equipe.html")

@app.route('/login/', methods=["GET","POST"])
def login():
    if request.method == "POST":
        if "senhaADM" in request.form:
            ra = "admin"
            senha = request.form["senhaADM"]
            if senha == "admin123":
                session["RA"] = ra  # Armazena o RA na sessão
                flash("Login de ADMINISTRADOR realizado com sucesso!", "success")
                return redirect(url_for("home"))
            else:
                flash("Senha incorreta!", "danger")
        else:
            ra = request.form["login"]
            senha = request.form["senha"]
            usuarios = carregar_usuarios()  # Carrega os usuários do MySQL
            for user in usuarios:
                if ra == user['ra']:  # Verifica se algum user tem o RA digitado
                    senha_bytes = senha.encode('utf-8')
                    senha_armazenada = user["senha"].encode('utf-8')  # Converter para bytes
                    if bcrypt.checkpw(senha_bytes, senha_armazenada):  # Comparar senha digitada com a senha no banco
                        session["RA"] = ra  # Armazena o RA na sessão
                        nome = user["nome"]
                        nome = nome.split()
                        session["nome"] = nome[0] + " " + nome[-1] if len(nome) > 1 else nome[0]
                        flash("Login realizado com sucesso!", "success")  # toast para mostrar na tela
                        return redirect(url_for("home"))
            flash("RA ou senha incorretos!", "danger")  # toast para mostrar na tela
            return redirect(url_for("home"))
    return render_template('/user/login.html')

@app.route('/cadastro/')
def cadastro():
    if(session.get("RA") and session.get("senha")):  # verifica se o existe o login e senha do user na sessão atual
        return render_template(url_for("home"))  # se tiver, envia para a rota do parametro
    else:
        return render_template("/user/cadastro.html") 

@app.route("/logout/")
def logout():
    session.clear()  # Remove todos os dados da sessão
    return redirect(url_for("home"))

@equipes_bp.route('/flash-message', methods=['POST'])
def flash_message():
    data = request.get_json()
    message = data.get('message', 'Algo deu errado!')
    category = data.get('category', 'info')
    return jsonify({"success": True, "message": message, "category": category}), 200

# Pega as rotas da parte de controlar usuarios e adiciona o prefixo /usuario
app.register_blueprint(usuarios_bp, url_prefix="/usuario/")
app.register_blueprint(atestados_bp, url_prefix="/atestado/")
app.register_blueprint(equipes_bp, url_prefix="/equipe/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)