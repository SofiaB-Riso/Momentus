from flask import Blueprint, jsonify, request

from services.google_places_service import GooglePlacesIndisponivel, buscar_fornecedores_perto

catalogo_controller = Blueprint("catalogo_controller", __name__)


@catalogo_controller.get("/catalogo/perto")
def fornecedores_perto():
    categoria = (request.args.get("categoria") or "todos").strip().lower()
    termo = (request.args.get("q") or "").strip() or None
    cidade = (request.args.get("cidade") or "").strip() or None
    lat = request.args.get("lat", type=float)
    lng = request.args.get("lng", type=float)

    tem_coordenadas = lat is not None and lng is not None
    if not tem_coordenadas and not cidade:
        return jsonify({"erro": "Informe sua localização (lat/lng) ou digite uma cidade."}), 400

    try:
        fornecedores = buscar_fornecedores_perto(
            categoria, lat=lat, lng=lng, cidade=cidade, termo=termo,
        )
    except GooglePlacesIndisponivel as erro:
        return jsonify({"erro": str(erro)}), 502

    return jsonify(fornecedores)
