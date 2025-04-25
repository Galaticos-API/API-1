from flask import Blueprint, request, session, jsonify, flash
import json
import os
import time
from datetime import datetime, timedelta

atestados_bp = Blueprint("atestados", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

atestados_FILE_PATH = os.path.join(BASE_DIR+"\\JSON\\", 'atestados.json')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
JSON_FILE = os.path.join(BASE_DIR+"\\JSON\\", 'uploads.json')

if not os.path.exists(BASE_DIR+"/JSON/"):
    os.makedirs(BASE_DIR+"/JSON/")  # Cria a pasta se ela não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Cria a pasta se ela não existir
# Garante que o arquivo JSON existe
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as f:
        json.dump([], f)  # Cria uma lista vazia no JSON


ALLOWED_EXTENSIONS = {'pdf'}  # Definição das extensões permitidas

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_to_json(filename, file_path, user, duration):
    if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Carrega os dados existentes
    else:
        data = []
        with open(JSON_FILE, 'w') as f:
            json.dump([], f)  # Cria uma lista vazia no JSON

    # Adiciona um novo registro com informações do usuário
    data.append({
        "filename": filename,
        "uploaded_by": user,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "duration": int(duration)
    })

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)  # Salva os dados atualizados

def is_duplicate(filename, user):
    if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return any(entry['filename'] == filename and entry['uploaded_by'] == user for entry in data)
    else:
        with open(JSON_FILE, 'w') as f:
            json.dump([], f)  # Cria uma lista vazia no JSON

@atestados_bp.route('/upload/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:  # Verifica se o arquivo foi recebido
        return "Nenhum arquivo enviado!", 400

    file = request.files['file']  # Obtém o arquivo do formulário
    if file.filename == '':  # Verifica se o usuário selecionou um arquivo
        return "Nenhum arquivo selecionado!", 400
    
    if not allowed_file(file.filename):  # Verifica a extensão
        return "Apenas arquivos PDF são permitidos!", 400
    
    if  not request.values.get('duration'): # verifica se a duração foi recebida
        return "duração não recebida", 400
    
    duration = request.values.get('duration') # Salva a duração
    
    if duration == 0: # Verifica se a duração é igual a zero
        return "A duração não pode ser zero", 400
    
    # Obtém o usuário logado
    user = session.get("RA")
    if not user:
        return "Usuário não autenticado!", 403
    
    # Evitar sobrescrever e gerar nome único
    timestamped_filename = f"{int(time.time())}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, timestamped_filename)
    

    # if is_duplicate(file.filename, user):
    #     return "Você já enviou esse arquivo anteriormente!", 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)  
    file.save(file_path)  # Salva o arquivo na pasta

    # Salva os detalhes do arquivo no JSON, incluindo o usuário logado
    save_to_json(file.filename, file_path, user, duration)
    flash(f"Documento {file.filename} enviado com sucesso!", "success")
    return jsonify({"message": f"Documento {file.filename} enviado com sucesso!"}), 201


@atestados_bp.route('/lista/', methods=['GET'])
# @login_required (exige login)
def recuperar_atestados():
    # Carrega os dados
    if not os.path.exists(JSON_FILE):
        return jsonify({"mensagem": "Nenhum atestado encontrado."}), 200

    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            atestados = json.load(f)

        # Filtros
        aluno = request.args.get('aluno', '').lower()
        data = request.args.get('data', '')

        if aluno:
            atestados = [a for a in atestados if aluno in a.get('aluno', '').lower()]
        if data:
            atestados = [a for a in atestados if a.get('data') == data]

        # Paginação
        pagina = int(request.args.get('pagina', 1))
        tamanho = int(request.args.get('tamanho', 10))
        inicio = (pagina - 1) * tamanho
        fim = inicio + tamanho
        atestados_paginados = atestados[inicio:fim]

        return jsonify({
            "total": len(atestados),
            "pagina": pagina,
            "tamanho": tamanho,
            "dados": atestados_paginados
        }), 200

    except json.JSONDecodeError:
        return jsonify({"erro": "Erro ao buscar os atestados."}), 500
    except Exception as e:
        return jsonify({"erro": f"Erro interno do servidor: {str(e)}"}), 500