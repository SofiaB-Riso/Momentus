# Rastreabilidade das funcionalidades

Esta matriz corresponde aos 40 itens da seção Funcionalidades Implementadas do README. Cada leitura consulta o banco e cada alteração usa a transação do caso de uso. Os arquivos enviados têm metadados persistidos e conteúdo no armazenamento local.

| Nº | Caso de uso e interface | API Flask | Controller em classe | Service específico | Model / tabela |
|---|---|---|---|---|---|
| 1 | **Cadastrar conta** — `cadastro.html`, `#formCadastro` | `POST /auth/cadastro` | `AuthController.cadastro()` | `CadastroService` em `backend/services/conta/cadastro_service.py` | `Usuario` → `usuarios` |
| 2 | **Entrar na conta** — `index.html`, `#formLogin` | `POST /auth/login` | `AuthController.login()` | `LoginService` em `backend/services/conta/login_service.py` | `Usuario` → `usuarios` |
| 3 | **Atualizar perfil** — `configuracoes.html`, `#formPerfil` | `PUT /auth/perfil` | `AuthController.atualizar_perfil()` | `AtualizarPerfilService` em `backend/services/conta/atualizar_perfil_service.py` | `Usuario` → `usuarios` |
| 4 | **Excluir a própria conta** — `configuracoes.html`, `#botaoExcluirConta` | `DELETE /auth/conta` | `AuthController.excluir_conta()` | `ExcluirContaService` em `backend/services/conta/excluir_conta_service.py` | `Usuario` → `usuarios` |
| 5 | **Criar evento** — `planejar.html`, `#formPlanejar` | `POST /eventos` | `EventoController.criar_evento()` | `CriarEventoService` em `backend/services/evento/criar_evento_service.py` | `Evento` → `eventos` |
| 6 | **Listar eventos acessíveis** — `eventos.html`, `#grelhaEventos` | `GET /eventos` | `EventoController.listar_eventos()` | `ListarEventosService` em `backend/services/evento/listar_eventos_service.py` | `Evento` → `eventos` |
| 7 | **Consultar os detalhes de um evento** — `evento.html`, `#conteudoEvento` | `GET /eventos/<int:evento_id>` | `EventoController.buscar_evento_por_id()` | `BuscarEventoPorIdService` em `backend/services/evento/buscar_evento_por_id_service.py` | `Evento` → `eventos` |
| 8 | **Atualizar um evento** — `planejar.html`, `#formPlanejar` | `PUT /eventos/<int:evento_id>` | `EventoController.atualizar_evento()` | `AtualizarEventoService` em `backend/services/evento/atualizar_evento_service.py` | `Evento` → `eventos` |
| 9 | **Excluir um evento** — `evento.html`, `#botaoApagarEvento` | `DELETE /eventos/<int:evento_id>` | `EventoController.deletar_evento()` | `DeletarEventoService` em `backend/services/evento/deletar_evento_service.py` | `Evento` → `eventos` |
| 10 | **Cadastrar convidado** — `evento.html`, `#formConvidado` | `POST /eventos/<int:evento_id>/convidados` | `ConvidadosController.adicionar_convidado()` | `AdicionarConvidadoService` em `backend/services/convidados/adicionar_convidado_service.py` | `Convidado` → `convidados` |
| 11 | **Atualizar a presença de convidado pelo painel** — `evento.html`, `.selectStatusConvidado` | `PUT /eventos/<int:evento_id>/convidados/<int:convidado_id>` | `ConvidadosController.atualizar_convidado()` | `AtualizarConvidadoService` em `backend/services/convidados/atualizar_convidado_service.py` | `Convidado` → `convidados` |
| 12 | **Remover convidado** — `evento.html`, `.linhaConvidado .botaoRemoverConvidado` | `DELETE /eventos/<int:evento_id>/convidados/<int:convidado_id>` | `ConvidadosController.remover_convidado()` | `RemoverConvidadoService` em `backend/services/convidados/remover_convidado_service.py` | `Convidado` → `convidados` |
| 13 | **Responder RSVP e informar restrições alimentares** — `rsvp.html`, `#formRsvp` | `POST /rsvp/<token>` | `ConvidadosController.responder_rsvp()` | `ResponderRsvpService` em `backend/services/convidados/responder_rsvp_service.py` | `Convidado` → `convidados` |
| 14 | **Convidar colaborador** — `evento.html`, `#formAdicionarColaborador` | `POST /eventos/<int:evento_id>/colaboradores` | `ColaboradoresController.adicionar_colaborador()` | `AdicionarColaboradorService` em `backend/services/colaboradores/adicionar_colaborador_service.py` | `ColaboradorEvento` → `colaboradores_evento` |
| 15 | **Aceitar ou recusar convite de colaboração** — `convite.html`, `#conviteAcoes` | `POST /colaboracoes/<token>/responder` | `ColaboradoresController.responder_colaboracao()` | `ResponderColaboracaoService` em `backend/services/colaboradores/responder_colaboracao_service.py` | `ColaboradorEvento` → `colaboradores_evento` |
| 16 | **Atualizar a permissão de um colaborador** — `evento.html`, `.permissaoColaborador` | `PUT /eventos/<int:evento_id>/colaboradores/<int:colaborador_id>` | `ColaboradoresController.atualizar_colaborador()` | `AtualizarColaboradorService` em `backend/services/colaboradores/atualizar_colaborador_service.py` | `ColaboradorEvento` → `colaboradores_evento` |
| 17 | **Remover colaborador** — `evento.html`, `.linhaColaborador .botaoRemoverConvidado` | `DELETE /eventos/<int:evento_id>/colaboradores/<int:colaborador_id>` | `ColaboradoresController.remover_colaborador()` | `RemoverColaboradorService` em `backend/services/colaboradores/remover_colaborador_service.py` | `ColaboradorEvento` → `colaboradores_evento` |
| 18 | **Adicionar item à lista compartilhada** — `evento.html`, `#formItemCompartilhado` | `POST /eventos/<int:evento_id>/itens-compartilhados` | `ItensController.criar_item_compartilhado()` | `CriarItemCompartilhadoService` em `backend/services/itens/criar_item_compartilhado_service.py` | `ItemCompartilhado` → `itens_compartilhados` |
| 19 | **Atribuir ou liberar o responsável por um item** — `evento.html`, `.botaoAssumirItem` | `PUT /eventos/<int:evento_id>/itens-compartilhados/<int:item_id>` | `ItensController.atualizar_item_compartilhado()` | `AtualizarItemCompartilhadoService` em `backend/services/itens/atualizar_item_compartilhado_service.py` | `ItemCompartilhado` → `itens_compartilhados` |
| 20 | **Remover item compartilhado** — `evento.html`, `.linhaItemCompartilhado .botaoRemoverConvidado` | `DELETE /eventos/<int:evento_id>/itens-compartilhados/<int:item_id>` | `ItensController.remover_item_compartilhado()` | `RemoverItemCompartilhadoService` em `backend/services/itens/remover_item_compartilhado_service.py` | `ItemCompartilhado` → `itens_compartilhados` |
| 21 | **Criar tarefa com prazo** — `evento.html`, `#formNovaTarefa` | `POST /eventos/<int:evento_id>/tarefas` | `TarefasController.adicionar_tarefa()` | `AdicionarTarefaService` em `backend/services/tarefas/adicionar_tarefa_service.py` | `TarefaEvento` → `tarefas_evento` |
| 22 | **Concluir ou reabrir uma tarefa** — `evento.html`, `.botaoAlternarTarefa` | `PUT /eventos/<int:evento_id>/tarefas/<int:tarefa_id>` | `TarefasController.atualizar_tarefa()` | `AtualizarTarefaService` em `backend/services/tarefas/atualizar_tarefa_service.py` | `TarefaEvento` → `tarefas_evento` |
| 23 | **Remover tarefa** — `evento.html`, `.botaoRemoverTarefa` | `DELETE /eventos/<int:evento_id>/tarefas/<int:tarefa_id>` | `TarefasController.remover_tarefa()` | `RemoverTarefaService` em `backend/services/tarefas/remover_tarefa_service.py` | `TarefaEvento` → `tarefas_evento` |
| 24 | **Registrar despesa** — `evento.html`, `#formDespesaEvento` | `POST /eventos/<int:evento_id>/despesas` | `FinanceiroController.adicionar_despesa()` | `AdicionarDespesaService` em `backend/services/financeiro/adicionar_despesa_service.py` | `DespesaEvento` → `despesas_evento` |
| 25 | **Anexar comprovante a uma despesa** — `evento.html`, `#comprovanteDespesaEvento` | `POST /eventos/<int:evento_id>/despesas/<int:despesa_id>/comprovante` | `FinanceiroController.enviar_comprovante()` | `EnviarComprovanteService` em `backend/services/financeiro/enviar_comprovante_service.py` | `DespesaEvento` → `despesas_evento` |
| 26 | **Excluir despesa** — `evento.html`, `.removerDespesa` | `DELETE /eventos/<int:evento_id>/despesas/<int:despesa_id>` | `FinanceiroController.remover_despesa()` | `RemoverDespesaService` em `backend/services/financeiro/remover_despesa_service.py` | `DespesaEvento` → `despesas_evento` |
| 27 | **Configurar o rateio das despesas** — `evento.html`, `#checkboxAtivarRateio` | `PUT /eventos/<int:evento_id>/rateio` | `FinanceiroController.definir_rateio()` | `DefinirRateioService` em `backend/services/financeiro/definir_rateio_service.py` | `Evento` → `eventos` |
| 28 | **Enviar foto para a galeria do evento** — `evento.html`, `#formFotoEvento` | `POST /eventos/<int:evento_id>/fotos` | `GaleriaController.enviar_foto()` | `EnviarFotoService` em `backend/services/galeria/enviar_foto_service.py` | `FotoEvento` → `fotos_evento` |
| 29 | **Remover foto da galeria** — `evento.html`, `.removerFotoEvento` | `DELETE /eventos/<int:evento_id>/fotos/<int:foto_id>` | `GaleriaController.remover_foto()` | `RemoverFotoService` em `backend/services/galeria/remover_foto_service.py` | `FotoEvento` → `fotos_evento` |
| 30 | **Gerar relatório do evento em PDF ou Excel** — `evento.html`, `#baixarPdfEvento` | `GET /eventos/<int:evento_id>/relatorio.pdf` | `RelatoriosController.relatorio_pdf()` | `ExportarRelatorioService` em `backend/services/relatorios/exportar_relatorio_service.py` | `Evento` → `eventos` |

## Regras comuns

- Eventos, convidados, tarefas, itens, despesas, fotos e colaboração validam o acesso pelo caso de uso antes de consultar ou alterar dados.
- A mesma conta pode criar eventos e aceitar convites; as permissões são definidas por evento, não por um cadastro separado de organizador.
- No item 7, a tela consulta explicitamente `GET /eventos/<id>`. A atualização ao vivo reutiliza essa consulta, mantendo as permissões e o preenchimento dos formulários.
- No item 11, o controle disponível é a presença; preferências sem saúde também podem ser editadas pelo painel, mediante declaração explícita. Saúde é informada somente pelo titular adulto no RSVP ou pelo responsável em link próprio. O RSVP do item 13 é um fluxo público separado, identificado por token individual.
- No item 19, atribuir e liberar são estados da atualização do responsável, contabilizados como um único caso de uso. Reservas concorrentes usam `ItemRepository`.
- No item 22, concluir e reabrir são estados de atualização da tarefa, contabilizados uma vez. A remoção do item 23 possui botão próprio e remove o registro real, sem recriar tarefas fictícias na interface.
- No item 25, o arquivo opcional é escolhido no formulário da despesa; após o cadastro, o frontend envia multipart para a rota do comprovante. A própria linha da despesa também permite anexar/substituir, inclusive após falha no envio. O banco guarda o vínculo com a despesa; referências a nomes de arquivo enviadas por JSON são recusadas.
- No item 30, PDF e Excel são formatos do mesmo caso de uso. O botão Excel chama `GET /eventos/<id>/relatorio.xlsx`, usando `RelatoriosController.relatorio_xlsx()` e o mesmo ExportarRelatorioService com outro exportador. O banco é consultado por RelatorioRepository.

## Repositories

`ConsultaEventoRepository` reúne consultas de acesso/listagem; `ItemRepository` faz a reserva condicional atômica; `RelatorioRepository` reúne dados dos relatórios. `AutorizacaoRepository` consome tokens de responsáveis atomicamente e `RequisicaoDespesaRepository` consulta/bloqueia envios idempotentes. O CRUD simples continua nas Models. `EventoRepository.buscar_por_tipo_evento()` mantém o CALL do MySQL encapsulado, com alternativa SQLite; essa rota adicional não foi usada para inflar a lista de funcionalidades da interface.

## Integração externa

As requisições do Google ficam em `BuscarLugaresGoogleService` e `BuscarFotoGoogleService`, em `services/integracoes`. O provider é um adaptador dos contratos e delega a comunicação a essas classes. A foto permanece um recurso legado de compatibilidade: os cards continuam coloridos e sem buscar imagens. As funções persistidas do projeto não dependem da disponibilidade ou da cota da API externa.

## Evidências

Os testes verificam as classes e rotas declaradas, o inventário do diagrama e os fluxos com SQLite temporário. A validação de navegador executa ações pela interface e confere requisições e registros persistidos. Consulte RESULTADO_TESTES.md para o que foi executado, seus resultados e limites.

## Novos fluxos de conta e privacidade

| Nº | Caso de uso e interface | API Flask | Controller em classe | Service específico | Model / tabela |
|---|---|---|---|---|---|
| 31 | **Enviar ou substituir foto de perfil** — `configuracoes.html`, `#arquivoAvatarConfig` | `POST /auth/foto` | `AuthController.alterar_foto()` | `AlterarFotoPerfilService` em `backend/services/conta/alterar_foto_perfil_service.py` | `PrivacidadeUsuario` → `privacidade_usuarios` |
| 32 | **Remover foto de perfil** — `configuracoes.html`, `#removerAvatarConfig` | `DELETE /auth/foto` | `AuthController.remover_foto()` | `RemoverFotoPerfilService` em `backend/services/conta/remover_foto_perfil_service.py` | `PrivacidadeUsuario` → `privacidade_usuarios` |
| 33 | **Solicitar recuperação de senha** — `recuperar-senha.html`, `#formRecuperarSenha` | `POST /auth/recuperacao` | `AuthController.solicitar_recuperacao()` | `SolicitarRecuperacaoService` em `backend/services/conta/solicitar_recuperacao_service.py` | `RecuperacaoSenha` → `recuperacoes_senha` |
| 34 | **Redefinir senha por link de uso único** — `redefinir-senha.html`, `#formRedefinirSenha` | `POST /auth/redefinir-senha` | `AuthController.redefinir_senha()` | `RedefinirSenhaService` em `backend/services/conta/redefinir_senha_service.py` | `RecuperacaoSenha` → `recuperacoes_senha` |
| 35 | **Registrar aceite dos termos** — `configuracoes.html`, `#formAceiteConfig` | `POST /privacidade/aceite` | `PrivacidadeController.aceitar()` | `AceitarTermosService` em `backend/services/conta/aceitar_termos_service.py` | `PrivacidadeUsuario` → `privacidade_usuarios` |
| 36 | **Exportar dados da própria conta em JSON** — `configuracoes.html`, `/privacidade/meus-dados` | `GET /privacidade/meus-dados` | `PrivacidadeController.exportar()` | `ExportarDadosService` em `backend/services/conta/exportar_dados_service.py` | `Usuario` → `usuarios` |

Os casos 33 e 34 dependem de SMTP real configurado para uso fora dos testes; a interface informa a indisponibilidade quando ele não está configurado. O aceite também integra o fluxo 1 de cadastro.


## Propostas, agenda, vagas e cronograma

| Nº | Caso de uso e interface | API Flask | Controller em classe | Service específico | Model / tabela |
|---|---|---|---|---|---|
| 37 | **Comparar propostas de fornecedores por custo e serviços** — `evento.html`, `#formCompararPropostas` | `GET /eventos/<int:evento_id>/propostas/comparacao` | `PropostasController.comparar()` | `CompararPropostasService` em `backend/services/propostas/comparar_propostas_service.py` | `PropostaFornecedor` → `propostas_fornecedor` |
| 38 | **Verificar conflitos de horário na agenda** — `planejar.html`, `#verificarConflitos` | `POST /eventos/conflitos` | `AgendaController.verificar()` | `VerificarConflitosAgendaService` em `backend/services/agenda/verificar_conflitos_service.py` | `Evento` → `eventos` |
| 39 | **Gerenciar vagas e promover automaticamente a lista de espera** — `evento.html`, `#formVagas` | `PUT /eventos/<int:evento_id>/lista-espera` | `ListaEsperaController.configurar()` | `ConfigurarVagasService` em `backend/services/lista_espera/configurar_vagas_service.py` | `EntradaEspera` → `entradas_espera` |
| 40 | **Gerar e recalcular o cronograma do evento** — `evento.html`, `#gerarCronograma` | `POST /eventos/<int:evento_id>/cronograma` | `CronogramaController.gerar()` | `GerarCronogramaService` em `backend/services/cronograma/gerar_cronograma_service.py` | `TarefaEvento` → `tarefas_evento` |

A comparação é uma consulta de negócio por categoria via PropostaRepository. O cadastro/edição/remoção que a alimenta não foi contado como três funcionalidades extras. AgendaRepository filtra apenas eventos acessíveis. ListaEsperaRepository organiza a fila por instante/id; OrganizarFilaService aplica a promoção sob bloqueio do evento. PlanejamentoEvento persiste duração, limite e ativação do cronograma. SincronizarCronogramaService aplica os prazos no cadastro/alteração do evento e GerarCronogramaService ativa a geração explícita. Todos os comandos passam por Controllers em classes e Services próprios, com validações e transação; as consultas especiais ficam nos Repositories.
