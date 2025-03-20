from flask import Flask, request, jsonify
import json
import bcrypt

app = Flask(__name__)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    ra = data.get('RA')
    tipo = data.get('tipo')
    
    if not nome or not email:
        return jsonify({"error": "Username and email are required"}), 400
    
    # Criptografar a senha
    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    # Armazenar os dados de usuários
    user = {"nome": nome, "email": email, "senha": hashed_senha.decode('utf-8'), "ra": ra, "tipo": tipo}
    
    try:
        # Deixar todos os dados registrados em um arquivo JSON
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    
    users.append(user)
    
    with open('users.json', 'w') as file:
        json.dump(users, file)
    
    return jsonify({"message": "User added successfully"}), 201

@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    
    return jsonify({"users": users}), 200

@app.route('/check_users_file', methods=['GET'])
def check_users_file():
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
        return jsonify({"users_file_content": users}), 200
    except FileNotFoundError:
        return jsonify({"error": "users.json file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON from users.json"}), 500

if __name__ == '__main__':
    app.run(debug=True)