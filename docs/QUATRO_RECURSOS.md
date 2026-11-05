# Propostas, conflitos, lista de espera e cronograma

Extensão de 03/11/2026 sobre o ZIP atualizado do grupo, sem IA e sem fotos do Google. Os números 37–40 ampliam a lista de casos de uso do README. São quatro fluxos com regras de negócio, além das operações básicas que os alimentam. A contagem e a classificação acadêmica final continuam dependendo dos critérios da disciplina.

## 37. Comparação de propostas

**Onde:** Todos os eventos → abrir evento → Comparar propostas.

1. Use o botão destacado Cadastrar proposta (o formulário também permanece aberto) e informe fornecedor, categoria, preço, desconto, taxas, parcelas e serviços inclusos. O campo de condições permite registrar particularidades reais do orçamento recebido.
2. Registre outra proposta da mesma categoria. Selecione os serviços necessários, um teto opcional e pressione Comparar propostas.
3. Opções com todos os serviços e dentro do teto aparecem primeiro; o destaque é a de menor total nesse grupo. Sem opção adequada, nenhuma recebe destaque. Propostas de categorias diferentes não são misturadas.
4. Edite/remova propostas pelos botões dos cards. Os dados permanecem após recarregar.

O total usa Decimal: preço − desconto + taxas. O desconto não pode superar o preço. As parcelas dividem os centavos; a primeira recebe um centavo extra se houver resto. O teto em branco usa o orçamento restante (orçamento menos despesas); se não há orçamento definido, não aplica teto. Um teto explícito de zero é respeitado. Registrar proposta não lança despesa nem efetua contratação. Valores e disponibilidade são fornecidos pelo usuário, sem consultas pagas ou preços inventados.

**Cadeia:** formulario/consulta → PropostasController → Criar/Atualizar/RemoverPropostaService ou CompararPropostasService → PropostaFornecedor / PropostaRepository → propostas_fornecedor. Somente dono/colaborador com edição altera propostas; leitor autorizado pode comparar.

## 38. Conflitos de agenda

**Onde:** Planejar evento (ou Editar) → data, horário, duração → Verificar conflitos na minha agenda.

A duração aceita 15–1440 minutos e é persistida em PlanejamentoEvento. Eventos antigos assumem 180 minutos até receberem configuração. A consulta compara intervalos dos eventos próprios/compartilhados ativos; exclui rascunhos, cancelados, concluídos e o evento em edição. A data completa e o horário formam cada intervalo; o mesmo horário em dias diferentes não gera conflito. A tela exibe o dia e o intervalo consultados. Terminar exatamente quando o outro começa não é sobreposição. Intervalos podem atravessar a meia-noite. O endereço/cidade normalizados são um sinal adicional, sem geocodificação. Eventos no período sem horário são contados separadamente. Alterar os campos invalida o resultado anterior.

É um aviso, sem impedir salvar: não consulta eventos privados de outras contas nem garante disponibilidade de um estabelecimento. Os horários são locais ao evento, conforme a convenção já usada pelo formulário.

**Cadeia:** botão → AgendaController → VerificarConflitosAgendaService → AgendaRepository / Evento e PlanejamentoEvento → eventos e planejamento_eventos.

## 39. Vagas e lista de espera automática

**Onde:** Evento → Convidados → Vagas e lista de espera; o convidado acompanha pelo link RSVP.

- Por padrão não há limite. A estimativa de convidados do planejamento não limita confirmações.
- Ative Limitar confirmações, informe o número e salve. Não é permitido reduzir abaixo do número já confirmado; ninguém perde a vaga silenciosamente.
- Ao confirmar além da capacidade, o convidado recebe status espera e posição privada. Reenviar a mesma confirmação não muda sua vez.
- Desistência, retorno a pendente ou exclusão de confirmado libera a vaga para a primeira pessoa elegível por instante de solicitação e id. Sair da fila e voltar coloca a pessoa no final.
- Aumentar/desativar o limite processa a fila imediatamente. A promoção gera aviso no convite e notificação interna da organização; não envia e-mail.
- Menor identificado precisa de autorização do responsável. Solicitar nova autorização retira a confirmação/fila e libera vaga. Uma promoção nunca ignora a autorização.
- O painel mostra a fila completa somente a pessoas com acesso ao evento. No RSVP, cada pessoa recebe sua posição; a privacidade da lista de confirmados continua obedecendo a configuração existente.
- Entrar na fila libera eventuais itens compartilhados assumidos; quem está em espera não pode reservar novos itens. Isso evita compromissos de quem ainda não tem vaga.

**Cadeia:** configurar no formulário → ListaEsperaController → ConfigurarVagasService; confirmar/desistir no RSVP → ConvidadosController → ResponderRsvpService. Os casos coordenam OrganizarFilaService, ListaEsperaRepository, EntradaEspera, Convidado e PlanejamentoEvento. O bloqueio do evento e a mesma transação serializam confirmações concorrentes, alterações de capacidade e promoções.

## 40. Cronograma sugerido

**Onde:** Evento → Tarefas → Gerar cronograma.

Gera seis etapas: local, fornecedores, cardápio, convites, confirmação dos convidados e revisão final. Reaproveita as quatro tarefas padrão existentes por chave, sem duplicá-las. Casamento, formatura, corporativo, aniversário e churrasco têm antecedências próprias; outros tipos usam o perfil genérico. Se há tempo suficiente, mantém as antecedências sugeridas. Se o evento está próximo, comprime proporcionalmente o perfil para distribuir as etapas entre hoje e a véspera, sem gerar prazos anteriores ao momento atual. Por exemplo: em 03/11, para casamento em 17/11, as etapas ficam em 03/11, 07/11, 12/11, 12/11, 15/11 e 16/11. A primeira respeita o horário atual se já passou das 09h. Para evento no mesmo dia, distribui pelo intervalo de horas restante até o início; sem horário, considera o fim do dia. Geração explícita para evento já iniciado/passado é recusada com mensagem. Alterações históricas para datas passadas não criam nem recalculam etapas.

Depois de ativado, mudar data/horário/tipo recalcula somente os prazos das tarefas automáticas pendentes. Tarefas concluídas e manuais mantêm seus prazos. Excluir uma etapa não faz ela reaparecer na próxima edição do evento; Regerar cronograma explícito repõe etapas faltantes. Gerar novamente não duplica etapas existentes. Para atualizar prazos gerados pela versão antiga, use Regerar cronograma; etapas concluídas e manuais continuam preservadas. O progresso continua sendo calculado sobre tarefas persistidas.

**Cadeia:** botão → CronogramaController → GerarCronogramaService → SincronizarCronogramaService → TarefaEvento e PlanejamentoEvento → tarefas_evento e planejamento_eventos. AtualizarEventoService também chama a sincronização quando data/tipo mudam. Somente quem pode editar o evento gera ou recalcula o cronograma.

## Atualizar e conferir

Não há novas dependências Python nem variáveis de ambiente. Inicie pelo Flask como já indicado no README. A aplicação cria as três tabelas novas com create_all; não adiciona colunas às tabelas antigas nem executa reset. Faça backup antes de atualizar outra instalação, conforme OPERACAO.md. O banco e os anexos originais do ZIP foram preservados; os testes usam cópias descartáveis.

Roteiro curto: compare duas propostas com serviços distintos; crie dois horários sobrepostos; limite a uma vaga e confirme duas pessoas em convites distintos, desistindo da primeira; gere o cronograma, conclua uma tarefa e altere a data. Recarregue para conferir persistência. Os testes reproduzíveis estão em backend/tests/test_quatro_recursos.py; os resultados desta entrega estão em RESULTADO_TESTES.md.
