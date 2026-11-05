from models import FavoritoFornecedor

from services.caso_uso import CasoUso


class ListarFavoritosService(CasoUso):
    def executar(self):
        usuario = self.usuario_atual()
        itens = FavoritoFornecedor.listar(usuario_id=usuario.id)
        return [f.chave for f in itens]
