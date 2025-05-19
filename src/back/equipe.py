from flask import Blueprint, Flask, request, jsonify, flash
import json
import os
import uuid

equipes_bp = Blueprint("equipes", __name__)

# para pegar o caminho certo do arquivo, pois esta sendo importado para o app.py
# e o caminho do arquivo é relativo ao app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EQUIPES_FILE_PATH = os.path.join(BASE_DIR+"\\JSON\\", 'equipes.json')
AVALIACOES_FILE_PATH = os.path.join(BASE_DIR+"\\JSON\\", 'avaliacoes.json')
USERS_FILE_PATH = os.path.join(BASE_DIR+"\\JSON\\", 'users.json')

if not os.path.exists(BASE_DIR+"/JSON/"):
    os.makedirs(BASE_DIR+"/JSON/")  # Cria a pasta se ela não existir
if not os.path.exists(EQUIPES_FILE_PATH):
    with open(EQUIPES_FILE_PATH, 'w') as f:
        json.dump([], f)  # Cria uma lista vazia no JSON
if not os.path.exists(AVALIACOES_FILE_PATH):
    with open(AVALIACOES_FILE_PATH, 'w') as f:
        json.dump([], f)  # Cria uma lista vazia no JSON

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
        
        #recupera o JSON de equipes
        if os.path.exists(EQUIPES_FILE_PATH) and os.path.getsize(EQUIPES_FILE_PATH) > 0:
            with open(EQUIPES_FILE_PATH, 'r') as file:
                equipes = json.load(file)
        else:
            equipes = []
        
        # Verifica conflitos de usuários em diversos grupos
        conflitos = []
        for membro in membros:
            id_usuario = membro.get("id_usuario")
            
            for equipe in equipes:
                membros_equipe = equipe.get("membros")
                for me in membros_equipe:
                    if id_usuario == me.get("id_usuario"): conflitos.append({"id_usuario": id_usuario, "nome": membro.get("nome")})
        
        # Se houver conflitos, retornamos erro
        if len(conflitos) > 0:
            flash("Conflitos ao criar equipe, algum usuário já está em outra equipe", "error")
            return jsonify({
                "success": False,
                "message": "Alguns membros já estão em outra equipe.",
                "conflitos": conflitos
            }), 400
        
        #objeto da equipe
        id_equipe = str(uuid.uuid4())
        equipe = {
            "id": id_equipe,
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

@equipes_bp.route('/remove_user', methods=['GET'])
def remove_user():
    ra = request.args.get("ra")
    id_equipe = request.args.get("id_equipe")
    
    try:
        if os.path.exists(EQUIPES_FILE_PATH) and os.path.getsize(EQUIPES_FILE_PATH) > 0:
            with open(EQUIPES_FILE_PATH, 'r') as file:
                equipes = json.load(file)
        else:
            equipes = []

        usuario_removido = False
        for equipe in equipes:
            if equipe.get("id") == id_equipe:
                membros_antes = len(equipe["membros"])
                equipe["membros"] = [m for m in equipe["membros"] if str(m.get("id_usuario")) != str(ra)]
                if len(equipe["membros"]) < membros_antes:
                    usuario_removido = True
                break  # já encontrou a equipe, pode sair do loop

        with open(EQUIPES_FILE_PATH, 'w') as file:
            json.dump(equipes, file)

        if usuario_removido:
            return jsonify({"message": "Usuário removido da equipe com sucesso"}), 200
        else:
            return jsonify({"message": "Usuário não encontrado na equipe"}), 404

    except Exception as e:
        return jsonify({"message": f"Erro ao remover usuário: {str(e)}"}), 500
    
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
                    membro["nome"] = nome[0] + " " + nome[-1] if len(nome) > 1 else nome[0]
        else:
            equipes = []
    except FileNotFoundError:
        equipes = []
    
    return jsonify({"equipes": equipes}), 200


@equipes_bp.route('/get_equipe_single', methods=['GET'])
def get_minha_equipe():
    id_usuario = request.args.get('id_usuario')

    if not id_usuario:
        return jsonify({"error": "Parâmetro 'id_usuario' é obrigatório"}), 400

    try:
        if os.path.exists(EQUIPES_FILE_PATH) and os.path.getsize(EQUIPES_FILE_PATH) > 0:
            with open(EQUIPES_FILE_PATH, 'r') as file:
                equipes = json.load(file)

            usuarios_dict = {u["ra"]: u["nome"] for u in users}

            for equipe in equipes:
                for membro in equipe.get("membros", []):
                    membro_id = membro.get("id_usuario")
                    nome = usuarios_dict.get(membro_id, "Desconhecido")
                    nome = nome.split()
                    membro["nome"] = (nome[0] + ' ' + nome[-1] if len(nome) > 1 else nome[0]) +' (' +membro.get("cargo") + ')'

                # Verifica se esse usuário faz parte da equipe
                if any(m["id_usuario"] == id_usuario for m in equipe.get("membros", [])):
                    return jsonify({"equipe": equipe}), 200

        return jsonify({"error": "Equipe não encontrada para esse usuário"}), 404
    
    except FileNotFoundError:
        return jsonify({"error": "Arquivo de equipes não encontrado"}), 500

@equipes_bp.route('/avaliar', methods=['POST'])
def avaliar():
    if request.method == "POST":
        data = request.get_json()
        membro = data.get('membro')
        sprint = data.get('sprint')
        avaliacao = data.get('avaliacao')
        obs = data.get('obs')
        
        dados = {
            "id_usuario" : membro,
            "sprint": sprint,
            "avaliacao": avaliacao,
            "obs": obs 
        }
        try:
            # Deixar todos os dados registrados em um arquivo JSON
            if os.path.exists(AVALIACOES_FILE_PATH) and os.path.getsize(AVALIACOES_FILE_PATH) > 0:
                with open(AVALIACOES_FILE_PATH, 'r') as file:
                    avaliacoes = json.load(file)
            else:
                avaliacoes = []
        except FileNotFoundError:
            avaliacoes = []
        
        avaliacoes.append(dados)
    
        with open(AVALIACOES_FILE_PATH, 'w') as file:
            json.dump(avaliacoes, file)
        
        flash("Avaliação registrada!", "success") # toast para mostrar na tela
        return jsonify({"message": "Avaliação Registrada"}), 201
    
    return jsonify({"message": "Erro ao receber dados"}), 400

@equipes_bp.route('/avaliacoes', methods=['GET'])
def listar_avaliacoes():
    try:
        if os.path.exists(AVALIACOES_FILE_PATH) and os.path.getsize(AVALIACOES_FILE_PATH) > 0:
            with open(AVALIACOES_FILE_PATH, 'r') as file:
                avaliacoes = json.load(file)
        else:
            avaliacoes = []
        return jsonify(avaliacoes), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao ler avaliações: {str(e)}"}), 500


@equipes_bp.route('/avaliacoes/<id_usuario>', methods=['GET'])
def listar_avaliacoes_por_usuario(id_usuario):
    try:
        if os.path.exists(AVALIACOES_FILE_PATH) and os.path.getsize(AVALIACOES_FILE_PATH) > 0:
            with open(AVALIACOES_FILE_PATH, 'r') as file:
                avaliacoes = json.load(file)
        else:
            avaliacoes = []

        # Filtra avaliações pelo ID do usuário
        filtradas = [av for av in avaliacoes if str(av.get("id_usuario")) == str(id_usuario)]

        # Sprints pré-definidas
        sprints = ["Sprint1", "Sprint2", "Sprint3"]
        
        # Estrutura os dados para se adequar ao formato do Highcharts
        formatted_data = {sprint: [] for sprint in sprints}

        for avaliacao in filtradas:
            sprint_name = f"Sprint{avaliacao.get('sprint', 0)}"
            if sprint_name in formatted_data:
                formatted_data[sprint_name] = list(avaliacao.get("avaliacao", {}).values())

        return jsonify(formatted_data), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao filtrar avaliações: {str(e)}"}), 500

    

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
