"""Registro explícito das ações de Controllers em classes nos Blueprints Flask."""


def registrar_controller(blueprint, classe, rotas):
    # Controllers não guardam dados da requisição em atributos. As ações usam
    # o contexto Flask e Services locais, sem compartilhar estado de usuários.
    controller = classe()
    for metodo, caminho, acao in rotas:
        blueprint.add_url_rule(
            caminho,
            endpoint=acao,
            view_func=getattr(controller, acao),
            methods=[metodo],
        )
