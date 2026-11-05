from application.contratos import Criado
from flask import Blueprint, request, session
from services.conta.alterar_foto_perfil_service import AlterarFotoPerfilService
from services.conta.atualizar_perfil_service import AtualizarPerfilService
from services.conta.cadastro_service import CadastroService
from services.conta.excluir_conta_service import ExcluirContaService
from services.conta.login_service import LoginService
from services.conta.perfil_service import PerfilService
from services.conta.redefinir_senha_service import RedefinirSenhaService
from services.conta.remover_foto_perfil_service import RemoverFotoPerfilService
from services.conta.solicitar_recuperacao_service import SolicitarRecuperacaoService
from utils.auth import iniciar_sessao, login_required

from controllers.contexto import obter_caso
from controllers.registro import registrar_controller
from controllers.respostas import ler_json, responder

auth_controller = Blueprint("auth_controller", __name__)


class AuthController:
    """Adaptador HTTP do recurso; regras de negócio ficam nos Services."""

    def _autenticar(self, classe):
        resultado = obter_caso(classe).executar(ler_json())
        dados = resultado.dados if isinstance(resultado, Criado) else resultado
        iniciar_sessao(dados["usuario"]["id"])
        return responder(resultado)

    def cadastro(self):
        return self._autenticar(CadastroService)

    def login(self):
        return self._autenticar(LoginService)

    def logout(self):
        session.clear()
        return "", 204

    def solicitar_recuperacao(self):
        return responder(obter_caso(SolicitarRecuperacaoService).executar(ler_json()))

    def redefinir_senha(self):
        resultado = obter_caso(RedefinirSenhaService).executar(ler_json())
        session.clear()
        return responder(resultado)

    @login_required
    def alterar_foto(self):
        return responder(
            obter_caso(AlterarFotoPerfilService).executar(request.files.get("foto"))
        )

    @login_required
    def remover_foto(self):
        return responder(obter_caso(RemoverFotoPerfilService).executar())

    @login_required
    def me(self):
        return responder(obter_caso(PerfilService).executar())

    @login_required
    def atualizar_perfil(self):
        return responder(obter_caso(AtualizarPerfilService).executar(ler_json()))

    @login_required
    def excluir_conta(self):
        resultado = obter_caso(ExcluirContaService).executar()
        session.clear()
        return responder(resultado)


registrar_controller(
    auth_controller,
    AuthController,
    [
        ("POST", "/auth/cadastro", "cadastro"),
        ("POST", "/auth/login", "login"),
        ("POST", "/auth/logout", "logout"),
        ("GET", "/auth/me", "me"),
        ("PUT", "/auth/perfil", "atualizar_perfil"),
        ("DELETE", "/auth/conta", "excluir_conta"),
        ("POST", "/auth/recuperacao", "solicitar_recuperacao"),
        ("POST", "/auth/redefinir-senha", "redefinir_senha"),
        ("POST", "/auth/foto", "alterar_foto"),
        ("DELETE", "/auth/foto", "remover_foto"),
    ],
)
