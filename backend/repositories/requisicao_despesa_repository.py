from models import RequisicaoDespesa, Usuario, db


class RequisicaoDespesaRepository:
    @staticmethod
    def bloquear_usuario(usuario_id):
        # A chave pertence à conta, inclusive quando dois envios usam eventos diferentes.
        db.session.execute(
            db.update(Usuario)
            .where(Usuario.id == usuario_id)
            .values(ativo=Usuario.ativo)
        )

    @staticmethod
    def por_chave(usuario_id, chave):
        return RequisicaoDespesa.query.filter_by(
            usuario_id=usuario_id, chave=chave
        ).first()
