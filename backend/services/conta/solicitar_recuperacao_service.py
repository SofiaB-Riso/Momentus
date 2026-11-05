from datetime import timedelta
from hashlib import sha256
from secrets import token_urlsafe

from models import RecuperacaoSenha
from models.tempo import utcnow
from repositories.recuperacao_senha_repository import RecuperacaoSenhaRepository
from repositories.usuario_repository import UsuarioRepository
from utils.validacao import normalizar_email, validar_entrada

from services.caso_uso import CasoUso


class SolicitarRecuperacaoService(CasoUso):
    def __init__(self, transacao, usuario_id, email):
        super().__init__(transacao, usuario_id)
        self.email = email

    def executar(self, dados):
        dados = validar_entrada(dados)
        endereco = normalizar_email(dados.get("email"))
        origem = self.email.verificar_configuracao()
        resposta = {
            "mensagem": "Se este e-mail estiver cadastrado, você receberá um link para redefinir sua senha."
        }
        usuario = UsuarioRepository.por_email(endereco, ativo=True)
        if not usuario:
            return resposta
        agora = utcnow()
        if (
            RecuperacaoSenhaRepository.solicitacoes_recentes(
                usuario.id, agora - timedelta(minutes=15)
            )
            >= 3
        ):
            return resposta
        token = token_urlsafe(32)
        RecuperacaoSenhaRepository.limpar_expiradas(agora - timedelta(days=1))
        RecuperacaoSenhaRepository.invalidar_pendentes(usuario.id, agora)
        RecuperacaoSenha(
            usuario_id=usuario.id,
            email=usuario.email,
            token_hash=sha256(token.encode()).hexdigest(),
            expira_em=agora + timedelta(minutes=30),
        ).salvar(confirmar=False)
        try:
            # Fragmento: o token não vai para logs HTTP nem para o Referer.
            self.email.executar(
                usuario.email, origem + "/redefinir-senha.html#token=" + token
            )
            self.transacao.confirmar()
        except Exception:
            self.transacao.reverter()
            raise
        return resposta
