from .database import db


class CrudModel:
    """CRUD básico nas Models, seguindo o exemplo da disciplina.

    confirmar=False permite agrupar entidade, avisos e histórico na mesma
    transação. O caso de uso confirma só depois de todas as regras passarem.
    """

    def salvar(self, confirmar=True):
        db.session.add(self)
        if confirmar:
            db.session.commit()
        return self

    def atualizar(self, confirmar=True, **campos):
        permitidos = set(self.__table__.columns.keys()) - {"id"}
        for campo, valor in campos.items():
            if campo not in permitidos:
                raise ValueError("Campo de atualização inválido.")
            setattr(self, campo, valor)
        return self.salvar(confirmar=confirmar)

    def deletar(self, confirmar=True):
        db.session.delete(self)
        if confirmar:
            db.session.commit()

    @classmethod
    def buscar_por_id(cls, identificador):
        return db.session.get(cls, identificador)

    @classmethod
    def buscar_um(cls, **campos):
        return cls.query.filter_by(**campos).first()

    @classmethod
    def listar(cls, **campos):
        return cls.query.filter_by(**campos).all()
