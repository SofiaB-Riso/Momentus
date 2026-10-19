from application.erros import NaoEncontrado
from models import ColaboradorEvento

from services.caso_uso import CasoUso


class VerColaboracaoService(CasoUso):
    def executar(self, token):
        """Exibe somente os dados necessários para a tela pública do convite."""
        colab = ColaboradorEvento.buscar_um(token=token)
        if not colab:
            raise NaoEncontrado("Convite de colaboração inválido ou expirado.")
        return {
            "colaborador": {
                "nome": colab.nome,
                "email": colab.email,
                "status": colab.status,
                "token": colab.token,
            },
            "evento": {
                "id": colab.evento.id,
                "nome": colab.evento.nome_evento,
                "data": colab.evento.data_evento.isoformat()
                if colab.evento.data_evento
                else None,
                "hora": colab.evento.hora_evento or "",
                "organizador": colab.evento.owner.nome
                if colab.evento.owner
                else "Momentus",
            },
        }
