from flask import Flask, session, redirect, url_for, render_template, request, flash
from cryptography.fernet import Fernet
from datetime import datetime
import secrets
import json
import os
import bcrypt

from back.user import usuarios_bp

key = Fernet.generate_key() # Gera a chave de criptografia
cipher_suite = Fernet(key)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
caminho_json  = os.path.join(BASE_DIR, 'back/users.json')

def carregar_usuarios(): # Função para carregar os usuários cadastrados
    try:
        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo) # retorna os users salvos no JSON
    except FileNotFoundError:
        return {}  # Retorna um dic vazio se o arquivo não existir

def verifyLogin(route):
    if session.get("RA"): # verifica se o user está logado
        return render_template(route) # se tiver, envia para a rota especificada
    else:
        return redirect(url_for("login")) # se nao estiver logado, vai para pagina de login


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
    
@app.route('/') # isso define uma rota
def home(): # funcao que é executada quando está na rota
   return verifyLogin("index.html") #envia o caminho do arquivo para a função verifyLogin
    
@app.route('/atestados/')
def atestado():
    return verifyLogin("atestados.html")

@app.route('/avaliacao/')
def avaliacao():
    return verifyLogin("avaliacao.html")

@app.route('/login/', methods=["GET","POST"])
def login():
    if request.method == "POST":
        # Captura os dados do formulário
        ra = request.form["login"]
        senha = request.form["senha"]
        
        usuarios = carregar_usuarios()  # Carrega os usuários do JSON
        for user in usuarios:
            if ra == user['ra']: # Verifica se algum user tem o RA digitado
                senha = senha.encode('utf-8')
                senha_armazenada = user["senha"].encode('utf-8')  # Converter para bytes
                
                if bcrypt.checkpw(senha, senha_armazenada): # Comparar senha digitada com a senha no JSON
                    session["RA"] = ra  # Armazena o RA na sessão
                    flash("Login realizado com sucesso!", "success") # toast para mostrar na tela
                    return redirect(url_for("home"))
        
        flash("RA ou senha incorretos!", "danger")  # toast para mostrar na tela
        return redirect(url_for("home"))
    
    return render_template('/user/login.html')

@app.route('/cadastro/')
def cadastro():
    if(session.get("RA") and session.get("senha")): # verifica se o existe o login e senha do user na sessão atual
        return render_template(url_for("home")) # se tiver, envia para a rota do parametro
    else:
        return render_template("/user/cadastro.html") 
    

@app.route("/logout/")
def logout():
    session.clear()  # Remove todos os dados da sessão
    return redirect(url_for("home"))

# Pega as rotas da parte de controlar usuarios e adiciona o prefixo /usuario
app.register_blueprint(usuarios_bp, url_prefix="/usuario")

if __name__ == '__main__':
    app.run(debug=True)



#tavão tentando criar uma rota para o upload dos PDFs

UPLOAD_FOLDER = 'uploads'  # Nome da pasta onde os PDFs serão salvos

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Cria a pasta se ela não existir
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Configura a pasta de upload

ALLOWED_EXTENSIONS = {'pdf'}  # Definição das extensões permitidas

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

JSON_FILE = 'uploads.json'  # Nome do arquivo JSON

# Garante que o arquivo JSON existe
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as f:
        json.dump([], f)  # Cria uma lista vazia no JSON

def save_to_json(filename, file_path, user):
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)  # Carrega os dados existentes

    # Adiciona um novo registro com informações do usuário
    data.append({
        "filename": filename,
        "file_path": file_path,
        "uploaded_by": user,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)  # Salva os dados atualizados

@app.route('/src/atestados/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:  # Verifica se o arquivo foi enviado
        return "Nenhum arquivo enviado!", 400

    file = request.files['file']  # Obtém o arquivo do formulário

    if file.filename == '':  # Verifica se o usuário selecionou um arquivo
        return "Nenhum arquivo selecionado!", 400
    
    if not allowed_file(file.filename):  # Verifica a extensão
        return "Apenas arquivos PDF são permitidos!", 400

    if file.mimetype != 'application/pdf':  # Verifica o tipo MIME
        return "O arquivo enviado não é um PDF válido!", 400

    # Obtém o usuário logado
    user = session.get("RA")
    if not user:
        return "Usuário não autenticado!", 403

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)  
    file.save(file_path)  # Salva o arquivo na pasta

    # Salva os detalhes do arquivo no JSON, incluindo o usuário logado
    save_to_json(file.filename, file_path, user)

    return f"Arquivo {file.filename} enviado com sucesso por {user}!"

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor Flask
    