from application.contratos import ProvedorFornecedores
from application.erros import DadosInvalidos
from application.erros import IntegracaoIndisponivel as GooglePlacesIndisponivel
from models import Fornecedor
from utils.mapas import links_mapa
from utils.validacao import normalizar

from services.caso_uso import CasoUso


class RecomendarFornecedoresService(CasoUso):
    def __init__(self, transacao, usuario_id, provedor: ProvedorFornecedores):
        super().__init__(transacao, usuario_id)
        self.provedor = provedor

    def executar(self, evento_id, params=None):
        _, evento = self.exigir_acesso_evento(evento_id)
        categoria = params.get("categoria", "buffet")
        if categoria not in {
            "buffet",
            "musica",
            "decoracao",
            "doces",
            "bebidas",
            "espacos",
        }:
            raise DadosInvalidos("Categoria inválida.")
        cidade = (params.get("cidade") or evento.cidade_evento or "").strip()[:120]
        if not cidade:
            raise DadosInvalidos(
                "Informe a cidade do evento para buscar recomendações."
            )
        estilo = (params.get("estilo") or evento.estilo_evento or "").strip()[:100]
        termo = {
            "buffet": "buffet",
            "musica": "música DJ banda",
            "decoracao": "decoração",
            "doces": "doces e bolos",
            "bebidas": "bar e bebidas",
            "espacos": "espaços para alugar",
        }[categoria]
        consulta = f"{termo} para {evento.tipo_evento} {estilo}"
        aviso = ""
        try:
            resultados = self.provedor.buscar(categoria, cidade=cidade, termo=consulta)
        except GooglePlacesIndisponivel:
            resultados = []
            aviso = "A busca externa está indisponível. Consulte as opções salvas ou tente novamente mais tarde."
        for fornecedor in Fornecedor.listar(ativo=True):
            if normalizar(cidade) not in normalizar(fornecedor.cidade):
                continue
            servico = normalizar(fornecedor.tipo_servico)
            palavras = {
                "espacos": ("espaco", "salao", "sitio"),
                "musica": ("musica", "dj", "banda"),
            }.get(categoria, (normalizar(categoria),))
            if not any((p in servico for p in palavras)):
                continue
            item = fornecedor.to_dict(incluir_usuario=False, incluir_produtos=False)
            item["fonte"] = "catalogo"
            resultados.append(item)
        for item in resultados:
            item["mapas"] = links_mapa(
                item.get("endereco") or item.get("nome_empresa"), cidade
            )
            item["motivo"] = (
                f"Busca por {evento.tipo_evento} em {cidade}; ordenação por avaliação."
            )
        resultados.sort(
            key=lambda item: (
                float(item.get("avaliacao") or 0),
                item.get("total_avaliacoes", 0),
            ),
            reverse=True,
        )
        return {
            "resultados": resultados[:12],
            "aviso": aviso,
            "cidade": cidade,
            "observacao": "Preço de locação, capacidade e disponibilidade precisam ser confirmados com o espaço."
            if categoria == "espacos"
            else "Consulte disponibilidade e orçamento com o fornecedor.",
        }
