from models import DespesaEvento, FotoEvento, PrivacidadeUsuario


class ArquivoRepository:
    @staticmethod
    def possui_referencias(nome):
        return any(
            (
                PrivacidadeUsuario.buscar_um(foto_arquivo=nome),
                FotoEvento.buscar_um(arquivo=nome),
                DespesaEvento.buscar_um(comprovante=nome),
            )
        )

    @staticmethod
    def referencias(nome):
        avatar = PrivacidadeUsuario.buscar_um(foto_arquivo=nome)
        foto = FotoEvento.buscar_um(arquivo=nome)
        despesa = DespesaEvento.buscar_um(comprovante=nome)
        return avatar, foto or despesa
