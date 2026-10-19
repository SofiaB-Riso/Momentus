from application.erros import Conflito, DadosInvalidos
from repositories.usuario_repository import UsuarioRepository
from utils.validacao import normalizar_email, validar_entrada

from services.caso_uso import CasoUso


class AtualizarPerfilService(CasoUso):
    def executar(self, dados):
        dados = validar_entrada(dados)
        usuario = self.usuario_atual()
        if "nome" in dados and (dados.get("nome") or "").strip():
            usuario.nome = dados["nome"].strip()
        if "telefone" in dados:
            usuario.telefone = (dados.get("telefone") or "").strip()
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
