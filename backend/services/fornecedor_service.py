from application.erros import NaoEncontrado
from models import Fornecedor
from repositories.fornecedor_repository import FornecedorRepository

from services.caso_uso import CasoUso


class ListarFornecedoresService(CasoUso):
    def executar(self, params):
        fornecedores = FornecedorRepository.pesquisar(
            (params.get("q") or "").strip(),
            (params.get("tipo") or "").strip(),
            (params.get("cidade") or "").strip(),
        )
        return [f.to_dict() for f in fornecedores]


class BuscarFornecedorService(CasoUso):
    def executar(self, fornecedor_id):
        fornecedor = Fornecedor.buscar_por_id(fornecedor_id)
        if not fornecedor or not fornecedor.ativo:
            raise NaoEncontrado("Fornecedor não encontrado.")
        return fornecedor.to_dict()
