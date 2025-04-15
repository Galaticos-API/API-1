from flask import Blueprint, Flask, request, jsonify, flash
import json, os, bcrypt, re

usuarios_bp = Blueprint("usuarios", __name__)

# para pegar o caminho certo do arquivo, pois esta sendo importado para o app.py
# e o caminho do arquivo é relativo ao app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE_PATH = os.path.join(BASE_DIR+"\\JSON\\", 'users.json')

if not os.path.exists(BASE_DIR+"/JSON/"):
    os.makedirs(BASE_DIR+"/JSON/")  # Cria a pasta se ela não existir

    # Função para carregar os usuários do arquivo
def carregar_usuarios():
    try:
        if os.path.exists(USERS_FILE_PATH) and os.path.getsize(USERS_FILE_PATH) > 0:
            with open(USERS_FILE_PATH, 'r') as file:
                return json.load(file)
        else:
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Função para salvar os usuários no arquivo
def salvar_usuarios(users):
    with open(USERS_FILE_PATH, 'w') as file:
        json.dump(users, file)

# Função para validar o formato do e-mail
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

# Função para validar a força da senha
def validar_senha(senha):
    if len(senha) < 6:
        return False
    if not re.search(r'[A-Za-z]', senha):  # Pelo menos uma letra
        return False
    if not re.search(r'\d', senha):        # Pelo menos um número
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):  # Pelo menos um caractere especial
        return False
    return True

@usuarios_bp.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    ra = data.get('login')

    # Validação dos campos obrigatórios
    if not nome or not email or not senha or not ra:
        return jsonify({"message": "Preencha todos os campos"}), 400
    
    # Validação do formato do e-mail
    if not validar_email(email):
        return jsonify({"message": "E-mail inválido"}), 400
    
    # Verificar se o e-mail ou RA já estão cadastrados
    users = carregar_usuarios()
    if any(user['email'] == email for user in users):
        return jsonify({"message": "E-mail já cadastrado"}), 400
    if any(user['ra'] == ra for user in users):
        return jsonify({"message": "RA já cadastrado"}), 400
    
    # Validação da senha
    if not validar_senha(senha):
        return jsonify({"message": "A senha deve ter pelo menos 6 caracteres"}), 400

    # Criptografar a senha
    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    # Armazenar os dados de usuários
    user = {"nome": nome, "email": email, "senha": hashed_senha.decode('utf-8'), "ra": ra}
    
    users.append(user)
    salvar_usuarios(users)
    
    with open(USERS_FILE_PATH, 'w') as file:
        json.dump(users, file)
        
    flash("Cadastro realizado com sucesso! Faça login", "success") # toast para mostrar na tela
    return jsonify({"message": "Cadastro realizado com sucesso"}), 201

@usuarios_bp.route('/get_users', methods=['GET'])
def get_users():
    try:
        if os.path.exists(USERS_FILE_PATH) and os.path.getsize(USERS_FILE_PATH) > 0:
            with open(USERS_FILE_PATH, 'r') as file:
                users = json.load(file)
                
        else:
            users = []
    except FileNotFoundError:
        users = []
    
    return jsonify({"users": users}), 200

@usuarios_bp.route('/check_users_file', methods=['GET'])
def check_users_file():
    try:
        with open(USERS_FILE_PATH, 'r') as file:
            users = json.load(file)
        return jsonify({"users_file_content": users}), 200
    except FileNotFoundError:
        return jsonify({"error": "users.json file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON from users.json"}), 500
