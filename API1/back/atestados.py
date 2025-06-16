from flask import Blueprint, request, session, jsonify, flash, send_from_directory
import mysql.connector
import os
import time
from datetime import datetime

atestados_bp = Blueprint("atestados", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Cria a pasta se ela não existir

ALLOWED_EXTENSIONS = {'pdf'}

from dotenv import load_dotenv
load_dotenv()
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_dict():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ra, nome FROM usuarios")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return {str(user['ra']): user['nome'] for user in users}

@atestados_bp.route('/validate/', methods=['POST'])
def validate_atestado():
    data = request.get_json()
    filename = data.get("filename")
    validation = data.get("validation")  # 'accept' ou 'deny'

    if not filename or validation not in ['accept', 'deny']:
        return jsonify({"message": "Parâmetros inválidos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    status = 'accepted' if validation == 'accept' else 'denied'
    cursor.execute("UPDATE uploads SET status=%s WHERE filename=%s", (status, filename))
    conn.commit()
    updated = cursor.rowcount
    cursor.close()
    conn.close()

    if updated:
        flash(f"Atestado {'aprovado' if validation == 'accept' else 'reprovado'} com sucesso!", "success")
        return jsonify({"message": f"Entry {filename} updated successfully!"}), 201
    else:
        flash(f"Erro ao realizar ação", "danger")
        return jsonify({"message": f"Entry {filename} not updated"}), 400

@atestados_bp.route('/upload/', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "Nenhum arquivo enviado!"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "Nenhum arquivo selecionado!"}), 400

        if not allowed_file(file.filename):
            return jsonify({"success": False, "message": "Apenas arquivos PDF são permitidos!"}), 400

        if not request.values.get('duration'):
            return jsonify({"success": False, "message": "Duração não recebida"}), 400

        if not request.values.get('filetype') or request.values.get('filetype') == 'undefined':
            return jsonify({"success": False, "message": "Tipo não especificado!"}), 400

        filetype = request.values.get('filetype')
        duration = request.values.get('duration')
        if int(duration) == 0:
            return jsonify({"success": False, "message": "A duração não pode ser zero"}), 400

        user = session.get("RA")
        if not user:
            return jsonify({"success": False, "message": "Usuário não autenticado!"}), 403

        timestamped_filename = f"{int(time.time())}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, timestamped_filename)
        file.save(file_path)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO uploads (filename, uploaded_by, timestamp, duration, status, filetype) VALUES (%s, %s, %s, %s, %s, %s)",
            (timestamped_filename, user, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), int(duration), 'undefined', filetype)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": f"Documento {file.filename} enviado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro interno: {str(e)}"}), 500
    
@atestados_bp.route('/lista/', methods=['GET'])
def recuperar_atestados():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM uploads")
    atestados = cursor.fetchall()
    cursor.close()
    conn.close()

    user_dict = get_user_dict()
    for atestado in atestados:
        atestado['name'] = atestado['filename']
        atestado['date'] = atestado['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(atestado['timestamp'], datetime) else str(atestado['timestamp'])
        atestado['file_url'] = f"/atestado/uploads/{atestado['filename']}"
        atestado['username'] = user_dict.get(str(atestado.get('uploaded_by')), atestado.get('uploaded_by'))

    return jsonify(atestados), 200

@atestados_bp.route('/lista_aluno/<ra>', methods=['GET'])
def recuperar_atestados_aluno(ra):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM uploads WHERE uploaded_by=%s", (ra,))
    atestados = cursor.fetchall()
    cursor.close()
    conn.close()

    user_dict = get_user_dict()
    for atestado in atestados:
        atestado['name'] = atestado['filename']
        atestado['date'] = atestado['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(atestado['timestamp'], datetime) else str(atestado['timestamp'])
        atestado['file_url'] = f"/atestado/uploads/{atestado['filename']}"
        atestado['username'] = user_dict.get(str(ra), ra)

    return jsonify(atestados), 200

@atestados_bp.route('/uploads/<filename>', methods=['GET'])
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)