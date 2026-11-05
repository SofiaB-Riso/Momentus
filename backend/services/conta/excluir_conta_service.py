from application.contratos import ArmazenamentoArquivos
from models import ColaboradorEvento, Evento
from repositories.usuario_repository import UsuarioRepository

from services.caso_uso import CasoUso
from services.galeria.arquivos_evento_service import ListarArquivosEventoService
from services.galeria.remover_arquivo_service import RemoverArquivoSemReferenciaService
from services.itens.liberacao_service import LiberarItensColaboradorService


class ExcluirContaService(CasoUso):
    def __init__(self, transacao, usuario_id, armazenamento: ArmazenamentoArquivos):
        super().__init__(transacao, usuario_id)
        self.armazenamento = armazenamento

    def executar(self):
        usuario = self.usuario_atual(exigir_autorizacao=False)
        arquivos = []
        if usuario.privacidade and usuario.privacidade.foto_arquivo:
            arquivos.append((usuario.privacidade.foto_arquivo, f"avatar{usuario.id}_"))
        for evento in Evento.listar(owner_id=usuario.id):
            arquivos.extend(ListarArquivosEventoService().executar(evento.id))
            evento.deletar(confirmar=False)
        for colaborador in ColaboradorEvento.listar(usuario_id=usuario.id):
            LiberarItensColaboradorService().executar(colaborador)
            colaborador.atualizar(confirmar=False, status="recusado")
        UsuarioRepository.desvincular_conta(usuario.id)
        usuario.deletar(confirmar=False)
        self.transacao.confirmar()
        for arquivo, prefixo in arquivos:
            RemoverArquivoSemReferenciaService(self.armazenamento).executar(
                arquivo, prefixo
            )
