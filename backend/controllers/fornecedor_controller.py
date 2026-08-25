from flask import Blueprint, jsonify, request
from sqlalchemy import or_

from models import Fornecedor, db

fornecedor_controller = Blueprint("fornecedor_controller", __name__)


# Estes dois endpoints são só de LEITURA: hoje eles consultam a tabela
# `fornecedores`, que futuramente será populada por uma integração com a
# API do Google (Places, por exemplo) em vez de cadastro manual do usuário.
# Por isso não existe mais rota de criação/edição de fornecedor por aqui.

@fornecedor_controller.get("/fornecedores")
def listar_fornecedores():
    termo = (request.args.get("q") or "").strip()
    tipo = (request.args.get("tipo") or "").strip()
    cidade = (request.args.get("cidade") or "").strip()

    consulta = Fornecedor.query.filter_by(ativo=True)
    if termo:
        like = f"%{termo}%"
        consulta = consulta.filter(or_(Fornecedor.nome_empresa.ilike(like), Fornecedor.descricao.ilike(like), Fornecedor.tipo_servico.ilike(like)))
    if tipo:
        consulta = consulta.filter(Fornecedor.tipo_servico.ilike(f"%{tipo}%"))
    if cidade:
        consulta = consulta.filter(Fornecedor.cidade.ilike(f"%{cidade}%"))

    fornecedores = consulta.order_by(Fornecedor.avaliacao.desc(), Fornecedor.nome_empresa.asc()).all()
    return jsonify([f.to_dict() for f in fornecedores])


@fornecedor_controller.get("/fornecedores/<int:fornecedor_id>")
def buscar_fornecedor(fornecedor_id):
    fornecedor = db.session.get(Fornecedor, fornecedor_id)
    if not fornecedor or not fornecedor.ativo:
        return jsonify({"erro": "Fornecedor não encontrado."}), 404
    return jsonify(fornecedor.to_dict())
