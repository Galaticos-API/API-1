from flask import Blueprint, Flask, request, jsonify
import json
import os
import bcrypt

usuarios_bp = Blueprint("usuarios", __name__)

# para pegar o caminho certo do arquivo, pois esta sendo importado para o app.py
# e o caminho do arquivo é relativo ao app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE_PATH = os.path.join(BASE_DIR, 'users.json')

@usuarios_bp.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    print(data)
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    ra = data.get('login')
    tipo = data.get('tipo')
    
    if not nome or not email or not senha or not ra or not tipo:
        return jsonify({"message": "Preencha todos os campos"}), 400
    
    # Criptografar a senha
    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    # Armazenar os dados de usuários
    user = {"nome": nome, "email": email, "senha": hashed_senha.decode('utf-8'), "ra": ra, "tipo": tipo}
    
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
