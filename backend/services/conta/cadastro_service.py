from application.contratos import Criado
from application.erros import Conflito, DadosInvalidos
from models import Usuario
from repositories.usuario_repository import UsuarioRepository
from utils.validacao import (
    normalizar_email,
    validar_entrada,
    validar_nome,
    validar_telefone,
)

from services.caso_uso import CasoUso
from services.conta.aceitar_termos_service import AceitarTermosService
from services.conta.declarar_idade_service import DeclararIdadeService
from services.conta.termos import VERSAO_TERMOS


class CadastroService(CasoUso):
    def executar(self, dados):
        dados = validar_entrada(dados)
        if (
            dados.get("aceite_termos") is not True
            or dados.get("versao_termos") != VERSAO_TERMOS
        ):
            raise DadosInvalidos(
                "Leia e aceite a versão atual dos Termos de Uso para criar sua conta."
            )
        nome = validar_nome(dados.get("nome"))
        email = normalizar_email(dados.get("email"))
        senha = dados.get("senha") or ""
        telefone = validar_telefone(dados.get("telefone"))
        if len(nome) < 2:
            raise DadosInvalidos("Informe seu nome completo.")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise DadosInvalidos("Informe um e-mail válido.")
        if len(senha) < 6:
            raise DadosInvalidos("A senha precisa ter pelo menos 6 caracteres.")
        if UsuarioRepository.por_email(email):
            raise Conflito("Já existe uma conta com este e-mail.")
        usuario = Usuario(nome=nome, email=email, telefone=telefone, tipo="cliente")
        usuario.definir_senha(senha)
        usuario.salvar(confirmar=False)
        self.transacao.sincronizar()
        DeclararIdadeService(self.transacao, usuario.id).executar(
            dados, confirmar=False
        )
        AceitarTermosService(self.transacao, usuario.id).executar(
            dados, confirmar=False
        )
        self.transacao.confirmar()
        return Criado({"usuario": usuario.to_dict()})
