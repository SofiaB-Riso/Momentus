class RelatorioRepository:
    @staticmethod
    def obter(evento):
        # Converte os relacionamentos persistidos em dados independentes do ORM.
        return {
            "nome": evento.nome_evento,
            "Resumo": [
                ["Evento", evento.nome_evento],
                ["Tipo", evento.tipo_evento],
                ["Data", evento.data_evento.strftime("%d/%m/%Y")],
                ["Local", evento.endereco_evento or "-"],
                ["Orçamento", float(evento.orcamento_evento or 0)],
                ["Gasto atual", evento.total_despesas],
                ["Confirmados", evento.confirmados],
            ],
            "Convidados": [["Nome", "E-mail", "Telefone", "Status", "Restrições"]]
            + [
                [c.nome, c.email, c.telefone, c.status, c.restricoes_alimentares]
                for c in evento.convidados_rel
            ],
            "Despesas": [["Descrição", "Categoria", "Valor", "Pago por", "Comprovante"]]
            + [
                [d.descricao, d.categoria, float(d.valor), d.pago_por, d.comprovante]
                for d in evento.despesas_rel
            ],
            "Itens": [["Item", "Categoria", "Quantidade", "Preço unitário", "Subtotal"]]
            + [
                [
                    i.nome,
                    i.categoria,
                    i.quantidade,
                    float(i.preco or 0),
                    float(i.preco or 0) * i.quantidade,
                ]
                for i in evento.itens_evento_rel
            ],
            "Lista compartilhada": [["Item", "Quantidade", "Responsável"]]
            + [
                [i.nome, i.quantidade, i.responsavel_nome]
                for i in evento.itens_compartilhados_rel
            ],
        }
