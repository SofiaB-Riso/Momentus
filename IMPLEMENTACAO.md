# Momentus — mapa de implementação dos requisitos

Este arquivo resume onde cada requisito funcional do trabalho está implementado.

| # | Requisito | Implementação principal |
|---|---|---|
| 1 | Gestão colaborativa de itens (junta-panelas) | `itens_compartilhados` no banco; rotas em `controllers/itens_controller.py`, casos de uso em `services/itens/` e operações atômicas em `repositories/item_repository.py`; reserva atômica, nome normalizado e liberação ao recusar/sair; convidado assume/libera pelo RSVP. |
| 2 | Rateio de despesas | Configuração `rateio_ativo`, `rateio_modo`, `rateio_valor_fixo`; rota `PUT /eventos/<id>/rateio`; cálculo único em `services/financeiro/resumo_financeiro_service.py`, divisão exata em centavos, exibida na tela do evento. |
| 3 | RSVP online | `convidados.token_rsvp`; páginas `rsvp.html`/`rsvp.js`; rotas públicas `GET/POST /rsvp/<token>` e SSE em `planejamento_controller.py`. |
| 4 | Notificações e lembretes | Tabela `notificacoes`; avisos de colaboração/RSVP/alterações; `avisos_convidado`; lembretes idempotentes de presença/itens/tarefas em `lembretes_service.py`. |
| 5 | Restrições alimentares | Campo `restricoes_alimentares` por convidado; editável no RSVP e resumido na área inteligente do evento. |
| 6 | Co-organizadores | Tabela `colaboradores_evento`; convite por token, aceite/recusa, permissão `pode_editar` e `logs_evento`, com autoria e aba Histórico para o dono. |
| 7 | Mapas | Endereço/cidade centralizados; Google Maps e Waze no painel, no RSVP e nas opções de espaços. |
| 8 | Recomendação de fornecedores | Google Places já existente, integrado ao evento por `/eventos/<id>/recomendacoes`; contexto de tipo/cidade/estilo e ordenação por avaliação; alternativa de registros legados. |
| 9 | Busca de locais | Busca externa e tabela `locais_evento` com orçamentos confirmados; `/eventos/<id>/locais` filtra orçamento, capacidade, cidade e estilo. |
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
- **Catálogo:** a interface atual consulta Google Places; modelos de fornecedores/produtos legados permanecem compatíveis. O cadastro usa uma única conta de usuário; as permissões de dono e colaborador continuam vinculadas a cada evento.

## Persistência

Dados de usuários, eventos, convidados, colaboradores, produtos, despesas, tarefas, fotos, favoritos, notificações e logs ficam no banco de dados. O `localStorage` é reservado a preferências de interface e cache de localização.


## Organização das camadas

- `controllers/`: controllers por recurso, preservando as rotas consumidas pelo frontend; `planejamento_controller.py` cuida do transporte SSE.
- `services/convidados/`, `services/colaboradores/`, `services/itens/`, `services/tarefas/`, `services/financeiro/`, `services/galeria/`, `services/locais/`, `services/relatorios/`: casos de uso específicos.
- `services/lembretes_service.py`: geração idempotente de lembretes; `services/atualizacoes_service.py`: dados e acesso para revisões ao vivo.
- `models/`: entidades e CRUD básico; `repositories/`: consultas específicas e atualizações atômicas.
- `application/`: contratos e composição; `infrastructure/`: Google, armazenamento de arquivos, transação e exportadores.
- `frontend/js/horario.js`: seletor de horário com relógio e controle do diálogo no planejamento.
- `frontend/js/evento-planejamento.js`: descoberta, comparação de espaços e histórico na interface existente.
- `backend/tests/test_colaboracao.py`: 19 testes originais de integração e concorrência.
- `backend/tests/test_regressao.py`: 21 testes adicionais de CRUD, erros, arquivos, relatórios, contratos, fronteiras de camada e horários válidos/inválidos.

- `backend/tests/test_catalogo_google.py`: 10 testes de busca sem fotos, Maps/Street View, ordenação por distância sem limite, coordenadas inválidas/zero, busca textual, antimeridiano e segurança do proxy legado.
- `frontend/js/script.js`: faixa de todos os eventos e ciclo de rascunho/finalização; rascunhos excluídos das estatísticas e calendário.
- `frontend/js/catalogo-google.js`: capas coloridas e links de Maps/Street View, sem fotos, com distância e busca por bairro/cidade.

O detalhamento da arquitetura e dos princípios SOLID está em [ARQUITETURA.md](ARQUITETURA.md). Os resultados executados estão em [RESULTADO_TESTES.md](RESULTADO_TESTES.md).


### Catálogo paginado — 19/10/2026

- `application/contratos.py`: contrato separado de busca paginada, preservando a busca em lista existente.
- `infrastructure/provedores/google_places.py`: cursor da próxima página, parâmetros estáveis e método em lista compatível.
- `services/catalogo_service.py`: validação compartilhada e caso de uso paginado com critérios estritos de avaliação.
- `controllers/catalogo_controller.py` e composição: seleção do caso de uso para `paginado=1`, sem mudar caminhos ou métodos HTTP.
- `frontend/js/catalogo-google.js`: filtro Melhores avaliados, acumulação, deduplicação, ordenação, botão de próxima página e descarte de respostas antigas.
- `backend/tests/test_catalogo_paginado.py`: 11 testes novos de paginação, limites, ordenação, compatibilidade e falhas. Onze testes de paginação.


### Identidade da sessão — 19/10/2026

- `utils/auth.py`: criação centralizada de sessão, vínculo ao cadastro e rejeição de cookies antigos ou de identidade divergente.
- `controllers/auth_controller.py`: login/cadastro usam a criação centralizada.
- `tests/test_identidade_sessao.py`: seis regressões para cookie legado, banco diferente com mesmo ID, ID alterado, reinício, perfil editado e credencial substituída.
- O teste de concorrência passa a reutilizar um cookie de login legítimo, em vez de fabricar uma sessão só com ID. A suíte atual inclui esses seis casos de identidade.


### Lotes de vinte cards — 19/10/2026

O frontend distingue cards visíveis, candidatos reservados e cursor remoto. Cada ação completa até vinte novos estabelecimentos únicos; páginas adicionais só são consultadas quando necessário para completar o lote. Reservas evitam exibir mais de vinte novos cards e são reutilizadas na ação seguinte. Cursores já visitados encerram ciclos. Buscas/filtros/localização novos limpam a reserva; falhas preservam candidatos e cursor para nova tentativa. Backend, regras de avaliação e vínculo de identidade da sessão foram mantidos.


### Limpeza atual

- `controllers/contexto.py` elimina a montagem repetida de casos de uso nos controllers.
- `CasoUso.exigir_acesso_evento` reúne a validação de existência/permissão; removidos aliases e retornos de erro inalcançáveis.
- `Evento.total_despesas_decimal` é a fonte do total de despesas e itens, também usada no rateio.
- `frontend/js/utils.js` reúne escape, estrelas e datas; `localizacao-momentus.js` reúne os controles repetidos de GPS/cidade.
- Ícones idênticos usam um único arquivo em `assets/icones`; estilos da tela de fornecedor descontinuada e funções sem consumidores foram retirados.
- A aplicação fixa `backend/instance` como diretório do SQLite padrão. A pasta da raiz foi removida e o banco entregue permanece sem registros.

A suíte atual tem 69 testes. `backend/tests/test_configuracao.py` verifica o caminho único do SQLite e a configuração de arquivo absoluto.
