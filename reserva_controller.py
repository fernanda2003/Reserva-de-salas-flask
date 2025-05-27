from flask import Blueprint, request, jsonify
from reserva_model import Reserva
from database import db
import requests

reserva_bp = Blueprint('reserva_bp', __name__)

API_ESCOLAR_URL = "http://192.168.15.5:5000/api/turma"

# Função para verificar se a turma existe na API externa
def validar_turma(turma_id):
    try:
        resposta = requests.get(f"{API_ESCOLAR_URL}/{turma_id}")
        return resposta.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Erro ao validar turma: {e}")
        return None  # Retorna None em vez de False para identificar erro de conexão

# Rota para criar nova reserva
@reserva_bp.route('/reservas', methods=['POST'])
def criar_reserva():
    data = request.json

    # Verifica se todos os campos obrigatórios estão presentes
    campos_obrigatorios = ["turma_id", "sala", "data", "hora_inicio", "hora_fim"]
    if not all(campo in data for campo in campos_obrigatorios):
        return jsonify({"erro": "Dados incompletos"}), 400

    turma_id = data["turma_id"]
    turma_valida = validar_turma(turma_id)

    if turma_valida is None:
        return jsonify({"erro": "Erro ao conectar com o serviço de turma"}), 503
    if not turma_valida:
        return jsonify({"erro": "Turma não encontrada"}), 404

    # Cria e salva a reserva
    reserva = Reserva(
        turma_id=turma_id,
        sala=data["sala"],
        data=data["data"],
        hora_inicio=data["hora_inicio"],
        hora_fim=data["hora_fim"]
    )
    db.session.add(reserva)
    db.session.commit()

    return jsonify({"mensagem": "Reserva criada com sucesso"}), 201

# Rota para listar todas as reservas
@reserva_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    reservas = Reserva.query.all()
    return jsonify([
        {
            "id": r.id,
            "turma_id": r.turma_id,
            "sala": r.sala,
            "data": r.data,
            "hora_inicio": r.hora_inicio,
            "hora_fim": r.hora_fim
        } for r in reservas
    ])
