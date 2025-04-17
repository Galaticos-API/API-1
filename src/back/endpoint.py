from flask import Blueprint, Flask, jsonify, request
from flask_login import login_required
import json, os

endpoint_bp = Blueprint('endpoint_bp', __name__)

CAMINHO_ATESTADOS = 'JSON/uploads.json'

@endpoint_bp.route('/back/JSON/uploads', methods=['GET'])
# @login_required (exige login)
def recuperar_atestados():
    # Carrega os dados
    if not os.path.exists(CAMINHO_ATESTADOS):
        return jsonify({"mensagem": "Nenhum atestado encontrado."}), 200

    try:
        with open(CAMINHO_ATESTADOS, 'r', encoding='utf-8') as f:
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
        return jsonify({"erro": "Erro ao processar os dados dos atestados."}), 500
    except Exception as e:
        return jsonify({"erro": f"Erro interno do servidor: {str(e)}"}), 500