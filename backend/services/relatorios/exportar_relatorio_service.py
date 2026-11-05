from application.contratos import ArquivoGerado, ExportadorRelatorio
from repositories.relatorio_repository import RelatorioRepository

from services.caso_uso import CasoUso


class ExportarRelatorioService(CasoUso):
    def __init__(
        self, transacao, usuario_id, exportador: ExportadorRelatorio, extensao, tipo
    ):
        super().__init__(transacao, usuario_id)
        self.exportador = exportador
        self.extensao = extensao
        self.tipo = tipo

    def executar(self, evento_id):
        _, evento = self.exigir_acesso_evento(evento_id)
        dados = RelatorioRepository.obter(evento)
        return ArquivoGerado(
            self.exportador.exportar(dados),
            f"momentus-evento-{evento.id}.{self.extensao}",
            self.tipo,
        )
