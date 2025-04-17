from flask import Blueprint, request, session, jsonify, flash
import json
import os
import time
from datetime import datetime

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

def save_to_json(filename, file_path, user):
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
        "file_path": file_path,
        "uploaded_by": user,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
    save_to_json(file.filename, file_path, user)
    flash(f"Documento {file.filename} enviado com sucesso!", "success")
    return jsonify({"message": f"Documento {file.filename} enviado com sucesso!"}), 201
