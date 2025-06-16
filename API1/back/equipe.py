from flask import Blueprint, request, jsonify, flash
import mysql.connector
import uuid

equipes_bp = Blueprint("equipes", __name__)

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


@equipes_bp.route('/add', methods=['POST'])
def add():
    try:
        data = request.get_json()
        nome = data.get("nome")
        membros = data.get("membros")

        if not nome or not membros:
            return jsonify({"success": False, "message": "Dados obrigatórios não informados"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        conflitos = []
        for membro in membros:
            id_usuario = membro.get("id_usuario")
            cursor.execute("SELECT equipe_id FROM membros_equipe WHERE id_usuario = %s", (id_usuario,))
            if cursor.fetchone():
                conflitos.append({"id_usuario": id_usuario, "nome": membro.get("nome")})

        if conflitos:
            cursor.close()
            conn.close()
            return jsonify({
                "success": False,
                "message": "Alguns membros já estão em outra equipe.",
                "conflitos": conflitos
            }), 400

        import uuid
        id_equipe = str(uuid.uuid4())
        cursor.execute("INSERT INTO equipes (id, nome) VALUES (%s, %s)", (id_equipe, nome))
        for membro in membros:
            cursor.execute(
                "INSERT INTO membros_equipe (equipe_id, id_usuario, cargo) VALUES (%s, %s, %s)",
                (id_equipe, membro.get("id_usuario"), membro.get("cargo"))
            )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "Cadastro realizado com sucesso"}), 201
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro interno: {str(e)}"}), 500
    
@equipes_bp.route('/remove', methods=['POST'])
def remove_equipe():
    data = request.get_json()
    id_equipe = data.get("id")
    if not id_equipe:
        return jsonify({"message": "ID da equipe não informado"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM membros_equipe WHERE equipe_id = %s", (id_equipe,))
    cursor.execute("DELETE FROM equipes WHERE id = %s", (id_equipe,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Equipe removida com sucesso"}), 200

@equipes_bp.route('/remove_user', methods=['POST'])
def remove_user():
    data = request.get_json()
    ra = data.get("ra")
    id_equipe = data.get("equipe_id")

    if not ra or not id_equipe:
        return jsonify({"message": "Parâmetros obrigatórios não informados"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM membros_equipe WHERE equipe_id = %s AND id_usuario = %s", (id_equipe, ra))
    usuario_removido = cursor.rowcount > 0

    # Remove avaliações do usuário removido
    cursor.execute("DELETE FROM avaliacoes WHERE id_usuario = %s", (ra,))
    conn.commit()
    cursor.close()
    conn.close()

    if usuario_removido:
        return jsonify({"message": "Usuário removido da equipe e avaliações excluídas com sucesso"}), 200
    else:
        return jsonify({"message": "Usuário não encontrado na equipe"}), 404

@equipes_bp.route('/get_equipes', methods=['GET'])
def get_equipes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM equipes")
    equipes = cursor.fetchall()

    # Busca membros de cada equipe
    for equipe in equipes:
        cursor.execute("SELECT m.id_usuario, u.nome, m.cargo FROM membros_equipe m JOIN usuarios u ON m.id_usuario = u.ra WHERE m.equipe_id = %s", (equipe["id"],))
        membros = cursor.fetchall()
        # Formata nome para "Primeiro Último"
        for membro in membros:
            nome = membro["nome"].split()
            membro["nome"] = nome[0] + " " + nome[-1] if len(nome) > 1 else nome[0]
        equipe["membros"] = membros

    cursor.close()
    conn.close()
    return jsonify({"equipes": equipes}), 200

@equipes_bp.route('/get_equipe_single', methods=['GET'])
def get_minha_equipe():
    id_usuario = request.args.get('id_usuario')
    if not id_usuario:
        return jsonify({"error": "Parâmetro 'id_usuario' é obrigatório"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.id, e.nome FROM equipes e
        JOIN membros_equipe m ON e.id = m.equipe_id
        WHERE m.id_usuario = %s
    """, (id_usuario,))
    equipe = cursor.fetchone()

    if not equipe:
        cursor.close()
        conn.close()
        return jsonify({"error": "Equipe não encontrada para esse usuário"}), 404

    cursor.execute("SELECT m.id_usuario, u.nome, m.cargo FROM membros_equipe m JOIN usuarios u ON m.id_usuario = u.ra WHERE m.equipe_id = %s", (equipe["id"],))
    membros = cursor.fetchall()
    for membro in membros:
        nome = membro["nome"].split()
        membro["nome"] = (nome[0] + ' ' + nome[-1] if len(nome) > 1 else nome[0]) + ' (' + membro.get("cargo") + ')'
    equipe["membros"] = membros

    cursor.close()
    conn.close()
    return jsonify({"equipe": equipe}), 200

@equipes_bp.route('/avaliar', methods=['POST'])
def avaliar():
    data = request.get_json()
    membro = data.get('membro')
    sprint = data.get('sprint')
    avaliacao = data.get('avaliacao')
    obs = data.get('obs')

    if not membro or not sprint or not avaliacao:
        return jsonify({"message": "Dados obrigatórios não informados"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO avaliacoes (id_usuario, sprint, avaliacao, obs) VALUES (%s, %s, %s, %s)",
        (membro, sprint, json.dumps(avaliacao), obs)
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Avaliação registrada!", "success")
    return jsonify({"message": "Avaliação Registrada"}), 201

@equipes_bp.route('/avaliacoes', methods=['GET'])
def listar_avaliacoes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM avaliacoes")
    avaliacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(avaliacoes), 200

@equipes_bp.route('/avaliacoes/<id_usuario>', methods=['GET'])
def listar_avaliacoes_por_usuario(id_usuario):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM avaliacoes WHERE id_usuario = %s", (id_usuario,))
    avaliacoes = cursor.fetchall()
    cursor.close()
    conn.close()

    # Sprints pré-definidas
    sprints = ["Sprint1", "Sprint2", "Sprint3"]
    formatted_data = {sprint: [] for sprint in sprints}

    for avaliacao in avaliacoes:
        sprint_name = f"Sprint{avaliacao.get('sprint', 0)}"
        if sprint_name in formatted_data:
            # Se o campo avaliacao for JSON string, converte para dict
            aval = avaliacao.get("avaliacao")
            if isinstance(aval, str):
                import json
                aval = json.loads(aval)
            formatted_data[sprint_name] = list(aval.values()) if aval else []

    return jsonify(formatted_data), 200