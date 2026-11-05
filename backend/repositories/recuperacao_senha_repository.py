from models import RecuperacaoSenha


class RecuperacaoSenhaRepository:
    @staticmethod
    def solicitacoes_recentes(usuario_id, desde):
        return RecuperacaoSenha.query.filter(
            RecuperacaoSenha.usuario_id == usuario_id,
            RecuperacaoSenha.criado_em >= desde,
        ).count()

    @staticmethod
    def invalidar_pendentes(usuario_id, agora):
        RecuperacaoSenha.query.filter_by(usuario_id=usuario_id, usado_em=None).update(
            {"usado_em": agora}, synchronize_session="fetch"
        )

    @staticmethod
    def consumir(token_hash, agora):
        # Uma única atualização condicional impede o reuso até em pedidos concorrentes.
        return (
            RecuperacaoSenha.query.filter(
                RecuperacaoSenha.token_hash == token_hash,
                RecuperacaoSenha.usado_em.is_(None),
                RecuperacaoSenha.expira_em > agora,
            ).update({"usado_em": agora}, synchronize_session="fetch")
            == 1
        )

    @staticmethod
    def limpar_expiradas(antes):
        RecuperacaoSenha.query.filter(RecuperacaoSenha.expira_em < antes).delete(
            synchronize_session=False
        )
