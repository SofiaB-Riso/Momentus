from application.erros import Conflito, DadosInvalidos
from repositories.usuario_repository import UsuarioRepository
from utils.validacao import (
    normalizar_email,
    validar_entrada,
    validar_nome,
    validar_telefone,
)

from services.caso_uso import CasoUso


class AtualizarPerfilService(CasoUso):
    def executar(self, dados):
        dados = validar_entrada(dados)
        usuario = self.usuario_atual(exigir_autorizacao=False)
        if "nome" in dados:
            usuario.nome = validar_nome(dados["nome"])
        if "telefone" in dados:
            usuario.telefone = validar_telefone(dados.get("telefone"))
        if "email" in dados:
            novo_email = normalizar_email(dados.get("email"))
            if "@" not in novo_email:
                raise DadosInvalidos("Informe um e-mail válido.")
            existe = UsuarioRepository.por_email(novo_email, exceto_id=usuario.id)
            if existe:
                raise Conflito("Este e-mail já está em uso.")
            usuario.email = novo_email
        self.transacao.confirmar()
        return {"usuario": usuario.to_dict()}
