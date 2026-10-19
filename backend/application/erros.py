"""Falhas dos casos de uso. A tradução para HTTP pertence aos controllers."""


class ErroAplicacao(Exception):
    def __init__(self, mensagem, **detalhes):
        super().__init__(mensagem)
        self.detalhes = detalhes


class DadosInvalidos(ErroAplicacao):
    pass


class NaoEncontrado(ErroAplicacao):
    pass


class Proibido(ErroAplicacao):
    pass


class NaoAutenticado(ErroAplicacao):
    pass


class Conflito(ErroAplicacao):
    pass


class IntegracaoIndisponivel(ErroAplicacao):
    pass
