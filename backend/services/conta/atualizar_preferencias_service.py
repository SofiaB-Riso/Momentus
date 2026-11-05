from application.erros import DadosInvalidos
from models import PreferenciasUsuario

from services.caso_uso import CasoUso


class AtualizarPreferenciasService(CasoUso):
    def executar(self, dados):
        if (
            not isinstance(dados, dict)
            or not dados
            or set(dados) - {"rsvp", "lembretes"}
        ):
            raise DadosInvalidos("Informe as preferências de RSVP e/ou lembretes.")
        if any(type(v) is not bool for v in dados.values()):
            raise DadosInvalidos("As preferências devem ser verdadeiras ou falsas.")
        usuario = self.usuario_atual(exigir_autorizacao=False)
        prefs = usuario.preferencias
        if prefs is None:
            prefs = PreferenciasUsuario(
                usuario_id=usuario.id, rsvp=True, lembretes=True
            ).salvar(confirmar=False)
            usuario.preferencias = prefs
        prefs.atualizar(confirmar=False, **dados)
        self.transacao.confirmar()
        return prefs.to_dict()
