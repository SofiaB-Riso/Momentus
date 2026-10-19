from application.erros import NaoAutenticado
from repositories.usuario_repository import UsuarioRepository
from utils.validacao import normalizar_email, validar_entrada

from services.caso_uso import CasoUso
from services.conta.convites_service import _vincular_convites_pendentes


class LoginService(CasoUso):
    def executar(self, dados):
        dados = validar_entrada(dados)
        email = normalizar_email(dados.get("email"))
        senha = dados.get("senha") or ""
        usuario = UsuarioRepository.por_email(email, ativo=True)
        if usuario is None or not usuario.conferir_senha(senha):
            raise NaoAutenticado("E-mail ou senha incorretos.")
        _vincular_convites_pendentes(usuario)
        self.transacao.confirmar()
        return {"usuario": usuario.to_dict()}
