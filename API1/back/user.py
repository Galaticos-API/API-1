from flask import Blueprint, request, jsonify, flash
import bcrypt
import re
import mysql.connector

usuarios_bp = Blueprint("usuarios", __name__)

from dotenv import load_dotenv
import os
load_dotenv()
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )


# Função para validar o formato do e-mail
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

# Função para validar a força da senha
def validar_senha(senha):
    if len(senha) < 6:
        return [False, "A senha deve ter pelo menos 6 caracteres"]
    if not re.search(r'[A-Za-z]', senha):  # Pelo menos uma letra
        return [False, "A senha deve conter pelo menos uma letra"]
    if not re.search(r'\d', senha):        # Pelo menos um número
        return [False, "A senha deve conter pelo menos um número"]
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):  # Pelo menos um caractere especial
        return [False, "A senha deve conter pelo menos um caractere especial"]
    return [True, "Senha válida"]

@usuarios_bp.route('/add', methods=['POST'])
def add():
    try:
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        ra = data.get('login')

        if not nome or not email or not senha or not ra:
            return jsonify({"success": False, "message": "Preencha todos os campos"}), 400

        if not validar_email(email):
            return jsonify({"success": False, "message": "E-mail inválido"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"success": False, "message": "E-mail já cadastrado"}), 400

        cursor.execute("SELECT * FROM usuarios WHERE ra = %s", (ra,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"success": False, "message": "RA já cadastrado"}), 400

        senha_valida = validar_senha(senha)
        if not senha_valida[0]:
            cursor.close()
            conn.close()
            return jsonify({"success": False, "message": senha_valida[1]}), 400

        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, ra) VALUES (%s, %s, %s, %s)",
            (nome, email, hashed_senha, ra)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Cadastro realizado com sucesso', 'success')
        return jsonify({"success": True, "message": "Cadastro realizado com sucesso"}), 201
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro interno: {str(e)}"}), 500
    
    
@usuarios_bp.route('/get_users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ra, nome, email FROM usuarios")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"users": users}), 200

@usuarios_bp.route('/check_users_file', methods=['GET'])
def check_users_file():
    # Apenas para compatibilidade, retorna todos os usuários do banco
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ra, nome, email FROM usuarios")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return