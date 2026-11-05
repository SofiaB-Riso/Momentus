from flask import Blueprint
from services.conta.aceitar_termos_service import AceitarTermosService
from services.conta.atualizar_preferencias_service import AtualizarPreferenciasService
from services.conta.consultar_autorizacao_service import (
    ConsultarAutorizacaoContaService,
)
from services.conta.consultar_privacidade_service import ConsultarPrivacidadeService
from services.conta.declarar_idade_service import DeclararIdadeService
from services.conta.exportar_dados_service import ExportarDadosService
from services.conta.gerar_autorizacao_service import GerarLinkResponsavelService
from services.conta.revogar_autorizacao_service import RevogarAutorizacaoContaService
from utils.auth import login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

privacidade_controller = Blueprint("privacidade_controller", __name__)


class PrivacidadeController:
    @login_required
    def autorizacao(self):
        return responder(obter_caso(ConsultarAutorizacaoContaService).executar())

    @login_required
    def declarar_idade(self):
        return responder(obter_caso(DeclararIdadeService).executar(ler_json()))

    @login_required
    def gerar_link(self):
        return responder(obter_caso(GerarLinkResponsavelService).executar())

    @login_required
    def revogar_autorizacao(self):
        return responder(obter_caso(RevogarAutorizacaoContaService).executar())

    @login_required
    def preferencias(self):
        return responder(obter_caso(AtualizarPreferenciasService).executar(ler_json()))

    def informacoes(self):
        return responder(obter_caso(ConsultarPrivacidadeService).executar())

    @login_required
    def aceitar(self):
        return responder(obter_caso(AceitarTermosService).executar(ler_json()))

    @login_required
    def exportar(self):
        resposta = responder(obter_caso(ExportarDadosService).executar())
        resposta.headers["Cache-Control"] = "private, no-store"
        return resposta


registrar_controller(
    privacidade_controller,
    PrivacidadeController,
    [
        ("GET", "/privacidade/autorizacao", "autorizacao"),
        ("PUT", "/privacidade/autorizacao", "declarar_idade"),
        ("POST", "/privacidade/autorizacao/link", "gerar_link"),
        ("DELETE", "/privacidade/autorizacao", "revogar_autorizacao"),
        ("PUT", "/privacidade/preferencias", "preferencias"),
        ("GET", "/privacidade/info", "informacoes"),
        ("POST", "/privacidade/aceite", "aceitar"),
        ("GET", "/privacidade/meus-dados", "exportar"),
    ],
)
