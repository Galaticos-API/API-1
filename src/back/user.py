from flask import Blueprint, Flask, request, jsonify, flash
import json
import os
import bcrypt

usuarios_bp = Blueprint("usuarios", __name__)

# para pegar o caminho certo do arquivo, pois esta sendo importado para o app.py
# e o caminho do arquivo é relativo ao app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE_PATH = os.path.join(BASE_DIR+"\\JSON\\", 'users.json')

if not os.path.exists(BASE_DIR+"/JSON/"):
    os.makedirs(BASE_DIR+"/JSON/")  # Cria a pasta se ela não existir

@usuarios_bp.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    ra = data.get('login')
    
    if not nome or not email or not senha or not ra:
        return jsonify({"message": "Preencha todos os campos"}), 400
    
    # Criptografar a senha
    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    # Armazenar os dados de usuários
    user = {"nome": nome, "email": email, "senha": hashed_senha.decode('utf-8'), "ra": ra}
    
    try:
        # Deixar todos os dados registrados em um arquivo JSON
        if os.path.exists(USERS_FILE_PATH) and os.path.getsize(USERS_FILE_PATH) > 0:
            with open(USERS_FILE_PATH, 'r') as file:
                users = json.load(file)
        else:
            users = []
    except FileNotFoundError:
        users = []
    
    users.append(user)
    
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
