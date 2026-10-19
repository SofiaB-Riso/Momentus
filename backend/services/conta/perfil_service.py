from services.caso_uso import CasoUso


class PerfilService(CasoUso):
    def executar(self):
        return {"usuario": self.usuario_atual().to_dict()}
