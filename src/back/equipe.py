from flask import Blueprint, Flask, request, jsonify, flash
import json
import os
import uuid

equipes_bp = Blueprint("equipes", __name__)

# para pegar o caminho certo do arquivo, pois esta sendo importado para o app.py
# e o caminho do arquivo é relativo ao app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EQUIPES_FILE_PATH = os.path.join(BASE_DIR+"\\JSON\\", 'equipes.json')
USERS_FILE_PATH = os.path.join(BASE_DIR+"\\JSON\\", 'users.json')

if not os.path.exists(BASE_DIR+"/JSON/"):
    os.makedirs(BASE_DIR+"/JSON/")  # Cria a pasta se ela não existir

users = []
try:
    if os.path.exists(USERS_FILE_PATH) and os.path.getsize(USERS_FILE_PATH) > 0:
        with open(USERS_FILE_PATH, 'r') as file:
            users = json.load(file)
    else:
        users = []
except FileNotFoundError:
    users = []


@equipes_bp.route('/add', methods=['POST'])
def add():
    if request.method == "POST":
        data = request.get_json()
        nome = data.get("nome")
        membros = data.get("membros")  # lista de dicts com id_usuario e cargo

        for m in membros:
            print(f"Usuário {m['id_usuario']} - Cargo: {m['cargo']}")

       
        

        # Armazenar os dados de usuários
        # ✅ Gerar um ID único
        equipe_id = str(uuid.uuid4())  # se quiser algo tipo: '2ff4-8be2...'
        equipe = {
            "id": equipe_id,
            "nome": nome,
            "membros": membros
        }
        
        
        try:
            # Deixar todos os dados registrados em um arquivo JSON
            if os.path.exists(EQUIPES_FILE_PATH) and os.path.getsize(EQUIPES_FILE_PATH) > 0:
                with open(EQUIPES_FILE_PATH, 'r') as file:
                    equipes = json.load(file)
            else:
                equipes = []
        except FileNotFoundError:
            equipes = []
        
        equipes.append(equipe)
    
        with open(EQUIPES_FILE_PATH, 'w') as file:
            json.dump(equipes, file)
        
        flash("Equipe criada com sucesso", "success") # toast para mostrar na tela
        return jsonify({"message": "Cadastro realizado com sucesso"}), 201
    
    return jsonify({"message": "Erro ao receber dados"}), 400



@equipes_bp.route('/get_equipes', methods=['GET'])
def get_equipes():
    try:
        if os.path.exists(EQUIPES_FILE_PATH) and os.path.getsize(EQUIPES_FILE_PATH) > 0:
            with open(EQUIPES_FILE_PATH, 'r') as file:
                equipes = json.load(file)
            
            usuarios_dict = {u["ra"]: u["nome"] for u in users}
            for equipe in equipes:
                for membro in equipe.get("membros", []):
                    id_usuario = membro.get("id_usuario")
                    nome = usuarios_dict.get(id_usuario, "Desconhecido")
                    nome = nome.split()
                    membro["nome"] = nome[0] + " " + nome[-1]
        else:
            equipes = []
    except FileNotFoundError:
        equipes = []
    
    return jsonify({"equipes": equipes}), 200



@equipes_bp.route('/check_equipes_file', methods=['GET'])
def check_equipes_file():
    try:
        with open(EQUIPES_FILE_PATH, 'r') as file:
            equipes = json.load(file)
        return jsonify({"equipes_file_content": equipes}), 200
    except FileNotFoundError:
        return jsonify({"error": "equipes.json file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON from equipes.json"}), 500
