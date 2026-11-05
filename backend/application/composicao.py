"""Escolha das implementações concretas na inicialização, fora dos casos de uso."""

import os

from infrastructure.arquivos.local import ArquivosLocal
from infrastructure.exportadores.excel import ExportadorExcel
from infrastructure.exportadores.pdf import ExportadorPDF
from infrastructure.provedores.google_places import GooglePlacesProvider
from infrastructure.transacao import TransacaoSQLAlchemy
from repositories.evento_repository import EventoRepository
from services.catalogo_service import (
    CatalogoPaginadoService,
    FornecedoresPertoService,
    FotoCatalogoService,
)
from services.conta.alterar_foto_perfil_service import AlterarFotoPerfilService
from services.conta.consultar_privacidade_service import ConsultarPrivacidadeService
from services.conta.excluir_conta_service import ExcluirContaService
from services.conta.remover_foto_perfil_service import RemoverFotoPerfilService
from services.conta.solicitar_recuperacao_service import SolicitarRecuperacaoService
from services.evento.buscar_eventos_por_tipo_service import BuscarEventosPorTipoService
from services.evento.deletar_evento_service import DeletarEventoService
from services.financeiro.enviar_comprovante_service import EnviarComprovanteService
from services.financeiro.remover_despesa_service import RemoverDespesaService
from services.galeria.enviar_foto_service import EnviarFotoService
from services.galeria.remover_foto_service import RemoverFotoService
from services.integracoes.enviar_email_service import EnviarEmailService
from services.locais.recomendar_fornecedores_service import (
    RecomendarFornecedoresService,
)
from services.relatorios.exportar_relatorio_service import ExportarRelatorioService


class Composicao:
    def __init__(self, config):
        self.config = config
        self.email = EnviarEmailService(config)
        self.transacao = TransacaoSQLAlchemy()
        self.busca_eventos = EventoRepository()
        self.arquivos = ArquivosLocal(config["UPLOAD_FOLDER"])
        self.provedor = GooglePlacesProvider(
            config.get("GOOGLE_MAPS_API_KEY", os.getenv("GOOGLE_MAPS_API_KEY")),
            config["SECRET_KEY"],
        )
        self.exportadores = {
            "pdf": (ExportadorPDF(), "application/pdf"),
            "xlsx": (
                ExportadorExcel(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
        }
        self.fabricas = {
            AlterarFotoPerfilService: lambda ator: AlterarFotoPerfilService(
                self.transacao, ator, self.arquivos
            ),
            RemoverFotoPerfilService: lambda ator: RemoverFotoPerfilService(
                self.transacao, ator, self.arquivos
            ),
            ConsultarPrivacidadeService: lambda ator: ConsultarPrivacidadeService(
                self.transacao, ator, self.config
            ),
            SolicitarRecuperacaoService: lambda ator: SolicitarRecuperacaoService(
                self.transacao, ator, self.email
            ),
            RemoverDespesaService: lambda ator: RemoverDespesaService(
                self.transacao, ator, self.arquivos
            ),
            DeletarEventoService: lambda ator: DeletarEventoService(
                self.transacao, ator, self.arquivos
            ),
            ExcluirContaService: lambda ator: ExcluirContaService(
                self.transacao, ator, self.arquivos
            ),
            BuscarEventosPorTipoService: lambda ator: BuscarEventosPorTipoService(
                self.transacao, ator, self.busca_eventos
            ),
            RemoverFotoService: lambda ator: RemoverFotoService(
                self.transacao, ator, self.arquivos
            ),
            EnviarFotoService: lambda ator: EnviarFotoService(
                self.transacao, ator, self.arquivos
            ),
            EnviarComprovanteService: lambda ator: EnviarComprovanteService(
                self.transacao, ator, self.arquivos
            ),
            RecomendarFornecedoresService: lambda ator: RecomendarFornecedoresService(
                self.transacao, ator, self.provedor
            ),
            FornecedoresPertoService: lambda ator: FornecedoresPertoService(
                self.transacao, ator, self.provedor
            ),
            CatalogoPaginadoService: lambda ator: CatalogoPaginadoService(
                self.transacao, ator, self.provedor
            ),
            FotoCatalogoService: lambda ator: FotoCatalogoService(
                self.transacao, ator, self.provedor
            ),
        }

    def caso(self, classe, usuario_id=None):
        if classe in self.fabricas:
            return self.fabricas[classe](usuario_id)
        return classe(self.transacao, usuario_id)

    def relatorio(self, extensao, usuario_id):
        exportador, tipo = self.exportadores[extensao]
        return ExportarRelatorioService(
            self.transacao, usuario_id, exportador, extensao, tipo
        )
