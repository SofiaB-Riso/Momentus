# Momentus — mapa de implementação dos requisitos

Este arquivo resume onde cada requisito funcional do trabalho está implementado.

| # | Requisito | Implementação principal |
|---|---|---|
| 1 | Gestão colaborativa de itens (junta-panelas) | `itens_compartilhados` no banco; CRUD em `evento_detalhes_controller.py`; convidado pode assumir/liberar item pelo próprio link RSVP sem ser colaborador. |
| 2 | Rateio de despesas | Configuração `rateio_ativo`, `rateio_modo`, `rateio_valor_fixo`; rota `PUT /eventos/<id>/rateio`; cálculo exibido na tela do evento. |
| 3 | RSVP online | `convidados.token_rsvp`; páginas `rsvp.html`/`rsvp.js`; rotas públicas `GET/POST /rsvp/<token>`. |
| 4 | Notificações e lembretes | Tabela `notificacoes`; avisos de colaboração/RSVP/alterações; lembretes de evento e tarefas próximas em `/notificacoes`. |
| 5 | Restrições alimentares | Campo `restricoes_alimentares` por convidado; editável no RSVP e resumido na área inteligente do evento. |
| 6 | Co-organizadores | Tabela `colaboradores_evento`; convite por token, aceite/recusa, permissão `pode_editar` e `logs_evento`. |
| 7 | Mapas | Endereço/cidade do evento e geração de link de busca no Google Maps no resumo do evento. |
| 8 | Recomendação de fornecedores | Contas de fornecedores + catálogo; `/eventos/<id>/resumo` recomenda prestadores de acordo com cidade/tipo. |
| 9 | Busca de locais | Fornecedores do tipo `Espaço` são destacados como opções de local no resumo inteligente, priorizando a cidade do evento. |
| 10 | Estimativa de orçamento base | `/eventos/<id>/resumo` gera projeção por alimentação, bebida, decoração e local conforme tipo e número estimado de convidados. |
| 11 | Cronograma dinâmico | Checklist/tarefas com prazo, ordem e status; progresso automático e lembretes de prazos. |
| 12 | Cadastro digital de convidados | CRUD completo com nome, e-mail, telefone, vínculo, status e link individual de RSVP. |
| 13 | Calculadora automática de suprimentos | Resumo calcula sugestões de comida/bebida usando confirmados/estimados. |
| 14 | Despesas reais | Tabela `despesas_evento`; cadastro de despesas e upload opcional de recibo/comprovante em imagem/PDF. |
| 15 | Teto de gastos | `orcamento_evento`; total real combina itens + despesas; o backend cria alerta quando o limite é ultrapassado. |
| 16 | Painel unificado | `inicio.html` e `evento.html` reúnem eventos, confirmados, tarefas, itens, financeiro e notificações. |
| 17 | Exportação de relatórios | Rotas `/relatorio.pdf` e `/relatorio.xlsx`, com convidados, despesas e listas de itens. |
| 18 | Galeria compartilhada | Tabela `fotos_evento`; upload/remoção de imagens na aba Galeria. |
| 19 | Privacidade da lista | `privacidade_convidados`: o dono escolhe se nomes confirmados aparecem no RSVP público. |
| 20 | Checklist pré-evento | Tarefas padrão ao criar evento + criação/edição/remoção e controle de conclusão. |

## Regras de acesso adotadas

- **Dono do evento:** é o usuário gravado em `eventos.owner_id`; pode editar/excluir o evento, convidar/remover colaboradores e definir permissões.
- **Colaborador:** é uma conta separada vinculada por convite; só entra na organização após aceitar e só altera dados quando `pode_editar = true`.
- **Convidado:** é uma pessoa vinculada ao evento, mas não precisa ter conta. Pode responder RSVP, informar restrições e assumir itens da lista compartilhada pelo token do convite. Não recebe acesso administrativo.
- **Fornecedor/parceiro:** possui conta própria e perfil comercial; cadastra produtos/serviços que aparecem no catálogo e nas recomendações.

## Persistência

Dados de usuários, eventos, convidados, colaboradores, produtos, despesas, tarefas, fotos, favoritos, notificações e logs ficam no banco de dados. O `localStorage` é reservado a preferências de interface, como tema, idioma e interruptores de configuração.
