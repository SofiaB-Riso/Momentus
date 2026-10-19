from application.contratos import ArmazenamentoArquivos
from models import ColaboradorEvento, Evento
from repositories.usuario_repository import UsuarioRepository

from services.caso_uso import CasoUso
from services.galeria.arquivos_evento_service import arquivos_do_evento
from services.itens.liberacao_service import liberar_itens_colaborador


class ExcluirContaService(CasoUso):
    def __init__(self, transacao, usuario_id, armazenamento: ArmazenamentoArquivos):
        super().__init__(transacao, usuario_id)
        self.armazenamento = armazenamento

    def executar(self):
        usuario = self.usuario_atual()
        arquivos = []
        for evento in Evento.listar(owner_id=usuario.id):
            arquivos.extend(arquivos_do_evento(evento.id))
            evento.deletar(confirmar=False)
        for colaborador in ColaboradorEvento.listar(usuario_id=usuario.id):
            liberar_itens_colaborador(colaborador)
            colaborador.atualizar(confirmar=False, status="recusado")
        UsuarioRepository.desvincular_conta(usuario.id)
        usuario.deletar(confirmar=False)
        self.transacao.confirmar()
        for arquivo in arquivos:
            self.armazenamento.remover(arquivo)
        return None
