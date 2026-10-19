from application.contratos import Criado
from flask import Blueprint, request, session
from services.conta.atualizar_perfil_service import AtualizarPerfilService
from services.conta.cadastro_service import CadastroService
from services.conta.excluir_conta_service import ExcluirContaService
from services.conta.login_service import LoginService
from services.conta.perfil_service import PerfilService
from utils.auth import iniciar_sessao, login_required

from controllers.contexto import obter_caso
from controllers.respostas import responder

auth_controller = Blueprint("auth_controller", __name__)


def _autenticar(classe):
    resultado = obter_caso(classe).executar(request.get_json(silent=True) or {})
    dados = resultado.dados if isinstance(resultado, Criado) else resultado
    iniciar_sessao(dados["usuario"]["id"])
    return responder(resultado)


@auth_controller.post("/auth/cadastro")
def cadastro():
    return _autenticar(CadastroService)


@auth_controller.post("/auth/login")
def login():
    return _autenticar(LoginService)


@auth_controller.post("/auth/logout")
def logout():
    session.clear()
    return "", 204


@auth_controller.get("/auth/me")
@login_required
def me():
    return responder(obter_caso(PerfilService).executar())


@auth_controller.put("/auth/perfil")
@login_required
def atualizar_perfil():
    return responder(
        obter_caso(AtualizarPerfilService).executar(request.get_json(silent=True) or {})
    )


@auth_controller.delete("/auth/conta")
@login_required
def excluir_conta():
    resultado = obter_caso(ExcluirContaService).executar()
    session.clear()
    return responder(resultado)
