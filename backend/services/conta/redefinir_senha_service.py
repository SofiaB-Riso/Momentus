from hashlib import sha256

from application.erros import DadosInvalidos
from models import RecuperacaoSenha, Usuario
from models.tempo import utcnow
from repositories.recuperacao_senha_repository import RecuperacaoSenhaRepository
from utils.validacao import validar_entrada

from services.caso_uso import CasoUso


class RedefinirSenhaService(CasoUso):
    def executar(self, dados):
        dados = validar_entrada(dados)
        token = dados.get("token")
        senha = dados.get("senha") or ""
        if len(senha) < 6 or len(senha) > 256:
            raise DadosInvalidos("A senha precisa ter entre 6 e 256 caracteres.")
        if not isinstance(token, str) or not 32 <= len(token) <= 100:
            raise DadosInvalidos("Link inválido ou expirado. Solicite outro e-mail.")
        digest = sha256(token.encode()).hexdigest()
        registro = RecuperacaoSenha.buscar_um(token_hash=digest)
        usuario = Usuario.buscar_por_id(registro.usuario_id) if registro else None
        if (
            not usuario
            or not usuario.ativo
            or usuario.email != registro.email
            or not RecuperacaoSenhaRepository.consumir(digest, utcnow())
        ):
            raise DadosInvalidos("Link inválido ou expirado. Solicite outro e-mail.")
        usuario.definir_senha(senha)
        RecuperacaoSenhaRepository.invalidar_pendentes(usuario.id, utcnow())
        self.transacao.confirmar()
        return {"mensagem": "Senha redefinida. Entre com sua nova senha."}
