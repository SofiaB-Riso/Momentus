from application.erros import DadosInvalidos
from models import FavoritoFornecedor
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso


class AlternarFavoritoService(CasoUso):
    def executar(self, dados=None):
        dados = validar_entrada(dados)
        usuario = self.usuario_atual()
        chave = (dados.get("chave") or "").strip()
        if not chave:
            raise DadosInvalidos("Chave do favorito é obrigatória.")
        favorito = FavoritoFornecedor.buscar_um(usuario_id=usuario.id, chave=chave)
        if favorito:
            favorito.deletar(confirmar=False)
            ativo = False
        else:
            FavoritoFornecedor(usuario_id=usuario.id, chave=chave).salvar(
                confirmar=False
            )
            ativo = True
        self.transacao.confirmar()
        return {"chave": chave, "favorito": ativo}
