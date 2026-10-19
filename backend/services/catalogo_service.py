from application.contratos import (
    ProvedorCatalogoPaginado,
    ProvedorFornecedores,
    ProvedorFotos,
)
from application.erros import DadosInvalidos

from services.caso_uso import CasoUso


class FornecedoresPertoService(CasoUso):
    def __init__(self, transacao, usuario_id, provedor: ProvedorFornecedores):
        super().__init__(transacao, usuario_id)
        self.provedor = provedor

    def executar(self, params):
        filtros = validar_filtros(params)
        categoria = filtros.pop("categoria")
        return self.provedor.buscar(categoria, **filtros)


def validar_filtros(params):
    categoria = (params.get("categoria") or "todos").strip().lower()
    termo = (params.get("q") or "").strip() or None
    cidade = (params.get("cidade") or "").strip() or None
    try:
        lat = float(params["lat"]) if params.get("lat") else None
        lng = float(params["lng"]) if params.get("lng") else None
    except (TypeError, ValueError):
        raise DadosInvalidos("Informe coordenadas válidas.") from None
    if (
        lat is not None
        and (not -90 <= lat <= 90)
        or (lng is not None and (not -180 <= lng <= 180))
    ):
        raise DadosInvalidos("Informe coordenadas válidas.")
    if (lat is None) != (lng is None):
        raise DadosInvalidos("Informe latitude e longitude juntas.")
    if (lat is None or lng is None) and (not cidade):
        raise DadosInvalidos("Informe sua localização (lat/lng) ou digite uma cidade.")
    return dict(categoria=categoria, lat=lat, lng=lng, cidade=cidade, termo=termo)


class CatalogoPaginadoService(CasoUso):
    def __init__(self, transacao, usuario_id, provedor: ProvedorCatalogoPaginado):
        super().__init__(transacao, usuario_id)
        self.provedor = provedor

    def executar(self, params):
        filtros = validar_filtros(params)
        pagina = params.get("pagina") or None
        if pagina is not None and (not isinstance(pagina, str) or len(pagina) > 8192):
            raise DadosInvalidos("Página de busca inválida. Faça a busca novamente.")
        melhores = filtros["categoria"] == "melhores"
        if melhores:
            filtros["categoria"] = "todos"
            # O Google arredonda minRating em passos de 0,5. A regra estrita é local.
            filtros["avaliacao_minima"] = 4.0
        resultado = self.provedor.buscar_pagina(**filtros, pagina=pagina)
        fornecedores = resultado["fornecedores"]
        if melhores:
            fornecedores = [
                f
                for f in fornecedores
                if type(f.get("avaliacao")) in (int, float)
                and f["avaliacao"] > 4
                and type(f.get("total_avaliacoes")) is int
                and f["total_avaliacoes"] > 200
            ]
            fornecedores.sort(
                key=lambda f: (
                    -f["avaliacao"],
                    -f["total_avaliacoes"],
                    f.get("distancia_metros") is None,
                    f.get("distancia_metros") or 0,
                )
            )
        return {
            "fornecedores": fornecedores,
            "proxima_pagina": resultado["proxima_pagina"],
        }


class FotoCatalogoService(CasoUso):
    def __init__(self, transacao, usuario_id, provedor: ProvedorFotos):
        super().__init__(transacao, usuario_id)
        self.provedor = provedor

    def executar(self, token):
        return self.provedor.foto(token)
