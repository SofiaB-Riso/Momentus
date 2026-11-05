from models import PropostaFornecedor


class PropostaRepository:
    @staticmethod
    def por_categoria(evento_id, categoria):
        return (
            PropostaFornecedor.query.filter_by(evento_id=evento_id, categoria=categoria)
            .order_by(PropostaFornecedor.id)
            .all()
        )
