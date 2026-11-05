from models import Fornecedor
from sqlalchemy import or_


class FornecedorRepository:
    @staticmethod
    def pesquisar(termo="", tipo="", cidade=""):
        consulta = Fornecedor.query.filter_by(ativo=True)
        if termo:
            like = f"%{termo}%"
            consulta = consulta.filter(
                or_(
                    Fornecedor.nome_empresa.ilike(like),
                    Fornecedor.descricao.ilike(like),
                    Fornecedor.tipo_servico.ilike(like),
                )
            )
        if tipo:
            consulta = consulta.filter(Fornecedor.tipo_servico.ilike(f"%{tipo}%"))
        if cidade:
            consulta = consulta.filter(Fornecedor.cidade.ilike(f"%{cidade}%"))
        return consulta.order_by(
            Fornecedor.avaliacao.desc(), Fornecedor.nome_empresa.asc()
        ).all()
