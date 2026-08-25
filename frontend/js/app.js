const Momentus = (() => {

    const CHAVE_TEMA = 'momentus:tema';
    const CHAVE_IDIOMA = 'momentus:idioma';
    const CHAVE_PREFS = 'momentus:preferencias';

    /* ================= TEMA ================= */

    function obterTema() {
        return localStorage.getItem(CHAVE_TEMA) || 'claro';
    }

    function aplicarTema(tema) {
        document.documentElement.setAttribute('data-tema', tema);
        localStorage.setItem(CHAVE_TEMA, tema);
        document.querySelectorAll('[data-controle-tema]').forEach((input) => {
            input.checked = tema === 'escuro';
        });
        const meta = document.querySelector('meta[name="theme-color"]');
        if (meta) meta.setAttribute('content', tema === 'escuro' ? '#0d0818' : '#f3f1fa');
    }

    function alternarTema() {
        aplicarTema(obterTema() === 'escuro' ? 'claro' : 'escuro');
    }

    /* ================= IDIOMA ================= */

    const IDIOMAS = {
        pt: {
            nomeIdioma: 'Português',
            navInicio: 'Início', navPlanejar: 'Planejar evento', navCatalogo: 'Catálogo', navConfig: 'Configurações', sair: 'Sair da conta',
            contaPremium: 'Conta Premium',
            buscaTopoPlaceholder: 'Buscar eventos, fornecedores...',
            rodapeMarca: 'Momentus — momentos planejados com carinho',
            rodapeDireitos: '© 2026 Momentus. Todos os direitos reservados.',

            iniPainel: 'Painel de controle',
            iniOla: 'Olá, {nome}!',
            iniSubtitulo0: 'Nenhum evento por enquanto. Que tal planejar o primeiro?',
            iniSubtitulo1: 'Você tem 1 evento se aproximando. Vamos deixar tudo pronto pra brilhar?',
            iniSubtituloN: 'Você tem {n} eventos se aproximando. Vamos deixar tudo pronto pra brilhar?',
            proximoEvento: 'Próximo evento',
            ultimaAlteracao: 'Última alteração há {n} dia(s)',
            criadoAgora: 'Criado agora há pouco',
            preparativos: 'Preparativos concluídos',
            semEventoTitulo: 'Nenhum evento planejado ainda',
            semEventoTexto: 'Toque em "Planejar evento" para criar o primeiro e acompanhar tudo por aqui.',
            planejarEvento: 'Planejar evento',
            planejarDescZero: 'Comece do zero e monte um evento inesquecível',
            planejarDescModelo: 'Use um modelo pronto e economize tempo',
            chipCasamento: 'Casamento', chipCorporativo: 'Corporativo', chipFormatura: 'Formatura',
            statEventosAtivos: 'Eventos ativos',
            statConvidados: 'Convidados confirmados',
            statDias: 'Dias até o próximo evento',
            statOrcamento: 'Orçamento reservado',
            calendario: 'Calendário',
            proximosEventos: 'Próximos eventos',
            semProximos: 'Nenhum evento agendado ainda.',
            statusConfirmado: 'Confirmado', statusPlanejamento: 'Em planejamento', statusAgendado: 'Agendado', statusRascunho: 'Rascunho',
            pesquisar: 'Pesquisar',
            buscaCatalogoPlaceholder: 'Salgadinhos, bolo, decoração...',

            planNovoEvento: 'Novo evento',
            planTitulo: 'Vamos planejar seu evento',
            planSubtitulo: 'Preencha os detalhes abaixo — você pode ajustar tudo depois.',
            planTipoEvento: 'Tipo de evento',
            catAniversario: 'Aniversário', catCasamento: 'Casamento', catChurrasco: 'Churrasco', catFormatura: 'Formatura', catCorporativo: 'Corporativo', catChaBebe: 'Chá de bebê',
            labelNomeEvento: 'Nome do evento', placeholderNomeEvento: 'Ex: Aniversário da Sofia',
            labelData: 'Data', labelHorario: 'Horário', placeholderHorario: '15:00',
            labelLocal: 'Local', placeholderLocal: 'Endereço ou nome do espaço',
            labelConvidados: 'Número de convidados', placeholderConvidados: '50',
            labelEstilo: 'Estilo', estiloIntimista: 'Intimista', estiloClassico: 'Clássico', estiloTematico: 'Temático', estiloArLivre: 'Ao ar livre',
            labelOrcamento: 'Orçamento estimado', ajudaOrcamento: '(arraste para ajustar)',
            labelObservacoes: 'Observações', placeholderObservacoes: 'Conte um pouco mais sobre o clima que você imagina para o evento...',
            botaoSalvarEvento: 'Salvar evento', botaoSalvarEventoOk: 'Evento salvo!',
            botaoRascunho: 'Salvar como rascunho', botaoRascunhoOk: 'Rascunho salvo!',
            resumoTitulo: 'Resumo do evento',
            resumoTipo: 'Tipo', resumoNome: 'Nome', resumoData: 'Data', resumoConvidados: 'Convidados', resumoOrcamento: 'Orçamento',
            resumoConvidadosSufixo: 'pessoas',
            checklistLocal: 'Escolha o local', checklistCardapio: 'Defina o cardápio no Catálogo', checklistConvites: 'Envie os convites', checklistFornecedores: 'Confirme os fornecedores',

            catFornecedores: 'Fornecedores & produtos',
            catTitulo: 'Catálogo',
            catSubtitulo: 'Tudo o que você precisa para montar o evento perfeito, em um só lugar.',
            catBuscaPlaceholder: 'Buscar pelo nome do estabelecimento...',
            filtroTodos: 'Todos', filtroSalgados: 'Salgados', filtroDoces: 'Doces', filtroBebidas: 'Bebidas', filtroDecoracao: 'Decoração', filtroBuffet: 'Buffet',

            confSuaConta: 'Sua conta',
            confTitulo: 'Configurações',
            confSubtitulo: 'Ajuste seu perfil, preferências e notificações.',
            confNomeCompleto: 'Nome completo', confEmail: 'E-mail', confTelefone: 'Telefone',
            confSalvarAlteracoes: 'Salvar alterações', confAlteracoesSalvas: 'Alterações salvas!',
            confNotificacoes: 'Notificações',
            confRsvpTitulo: 'Confirmações de convidados', confRsvpDesc: 'Receba um aviso a cada RSVP',
            confLembretesTitulo: 'Lembretes de eventos', confLembretesDesc: 'Alertas 48h antes de cada evento',
            confNovidadesTitulo: 'Novidades e promoções', confNovidadesDesc: 'Ofertas de fornecedores parceiros',
            confPreferencias: 'Preferências',
            confTemaEscuro: 'Tema escuro', confTemaEscuroDesc: 'Reduz o brilho da interface',
            confIdioma: 'Idioma', confIdiomaDesc: 'Português (Brasil)',
            confPagamento: 'Segurança da conta', confPagamentoDesc: 'Sessão protegida e dados persistidos no banco do Momentus', confAlterar: 'Alterar',
            confZonaRisco: 'Zona de risco',
            confExcluirTitulo: 'Excluir minha conta', confExcluirDesc: 'Essa ação é permanente e não pode ser desfeita', confExcluir: 'Excluir',

            verTodosEventos: 'Ver todos os eventos',
            todosEventosEyebrow: 'Seus eventos',
            todosEventosTitulo: 'Todos os eventos',
            todosEventosSubtitulo: 'Acompanhe, edite ou apague os eventos que você já planejou.',
            buscarEventosPlaceholder: 'Buscar por nome, local ou tipo...',
            nenhumEventoCriadoTitulo: 'Nenhum evento por aqui ainda',
            nenhumEventoCriadoTexto: 'Toque em "Planejar evento" para criar o primeiro.',
            botaoEditar: 'Editar',
            botaoApagar: 'Apagar',
            confirmarApagarEvento: 'Tem certeza que deseja apagar "{nome}"? Essa ação não pode ser desfeita.',
            cardEventoConvidados: 'convidados',
            voltarEventos: 'Voltar',
            voltarInicio: 'Voltar ao início',
            eventoNaoEncontradoTitulo: 'Evento não encontrado',
            eventoNaoEncontradoTexto: 'Esse evento pode ter sido apagado. Veja todos os seus eventos.',
            abaInformacoes: 'Informações',
            abaConvidados: 'Convidados',
            abaItens: 'Itens do catálogo',
            abaTarefas: 'Tarefas',
            detalhesEvento: 'Detalhes do evento',
            localDoEvento: 'Local',
            dataEHora: 'Data e horário',
            estiloDoEvento: 'Estilo',
            orcamentoEstimadoLabel: 'Orçamento estimado',
            orcamentoGastoLabel: 'Já reservado no catálogo',
            observacoesTitulo: 'Observações',
            semObservacoes: 'Nenhuma observação registrada.',
            convidadosTitulo: 'Lista de convidados',
            convidadosResumo: '{confirmados} confirmados · {pendentes} pendentes · {recusados} recusaram',
            nomeConvidadoLabel: 'Nome',
            contatoConvidadoLabel: 'Contato (e-mail ou telefone)',
            placeholderNomeConvidado: 'Nome do convidado',
            placeholderContatoConvidado: 'email@exemplo.com ou (31) 90000-0000',
            botaoAdicionarConvidado: 'Adicionar convidado',
            nenhumConvidado: 'Nenhum convidado adicionado ainda.',
            statusConvidadoPendente: 'Pendente',
            statusConvidadoConfirmado: 'Confirmado',
            statusConvidadoRecusado: 'Recusou',
            itensCatalogoTitulo: 'Itens do catálogo',
            itensCatalogoTexto: 'Produtos e fornecedores adicionados a este evento.',
            nenhumItemCatalogo: 'Nenhum item do catálogo adicionado ainda. Visite o Catálogo e use o botão "+".',
            irParaCatalogo: 'Ir para o catálogo',
            tarefasTitulo: 'Lista de tarefas',
            progressoPreparativos: 'Preparativos concluídos',
            escolherEventoTitulo: 'Adicionar a um evento',
            escolherEventoTexto: 'Escolha o evento em que deseja incluir "{produto}":',
            semEventosParaAdicionarTitulo: 'Você ainda não tem eventos',
            semEventosParaAdicionarTexto: 'Crie um evento primeiro para poder adicionar itens do catálogo a ele.',
            criarEventoAgora: 'Criar evento agora',
            itemAdicionadoEvento: 'Adicionado a "{evento}"!',
            filtroFavoritos: 'Favoritos ♥',
            nenhumFavorito: 'Você ainda não favoritou nenhum item. Toque no coração de um produto para salvá-lo aqui.',
            fecharModal: 'Fechar',
            totalItensEvento: 'Total em itens',
            removerItem: 'Remover',
            removerConvidadoAria: 'Remover convidado',
            editarEventoTitulo: 'Editar evento',
            salvarAlteracoesEvento: 'Salvar alterações',
            alteracoesSalvasEvento: 'Alterações salvas!',
            verEvento: 'Ver evento',

            abaColaboracao: 'Colaboração',
            colaboradoresTitulo: 'Colaboradores do evento',
            colaboradoresTexto: 'Convide pessoas para ajudar a organizar e dividir os itens deste evento.',
            botaoAdicionarColaborador: 'Adicionar colaborador',
            nenhumColaborador: 'Nenhum colaborador adicionado ainda.',
            statusColabPendente: 'Convite pendente',
            statusColabAtivo: 'Colaborador ativo',
            statusColabRecusado: 'Convite recusado',
            modalColaboradorTitulo: 'Adicionar colaborador',
            modalColaboradorTexto: 'Convide alguém para ajudar a organizar este evento e dividir os itens da lista compartilhada.',
            labelNomeColaborador: 'Nome',
            placeholderNomeColaborador: 'Nome do colaborador',
            labelEmailColaborador: 'E-mail',
            placeholderEmailColaborador: 'email@exemplo.com',
            botaoEnviarConviteEmail: 'Enviar convite por e-mail',
            botaoCopiarLinkConvite: 'Copiar link de convite',
            avisoLinkConvite: 'Compartilhe esse link por WhatsApp, e-mail ou onde preferir. Quem abrir vai poder aceitar o convite.',
            linkCopiado: 'Link copiado! Agora é só compartilhar.',
            linkNaoCopiado: 'Não foi possível copiar. Copie manualmente: {link}',
            conviteEnviadoEmail: 'Convite enviado para {email}. A pessoa vai receber um aviso para aceitar.',
            erroPreencherNomeColaborador: 'Digite o nome do colaborador.',
            erroPreencherEmailColaborador: 'Digite um e-mail para enviar o convite.',
            removerColaboradorAria: 'Remover colaborador',
            confirmarRemoverColaborador: 'Remover {nome} da lista de colaboradores?',
            reenviarConvite: 'Reenviar convite',
            conviteReenviado: 'Convite reenviado!',

            rateioTitulo: 'Rateio de despesas',
            rateioTexto: 'Divida o custo do evento entre você e os colaboradores ativos.',
            rateioAtivarLabel: 'Ativar rateio',
            rateioModoLabel: 'Como calcular o valor',
            rateioModoAuto: 'Automático (com base nas despesas totais)',
            rateioModoFixo: 'Valor fixo por pessoa',
            labelValorFixoRateio: 'Valor fixo por pessoa (R$)',
            placeholderValorFixoRateio: 'Ex: 50,00',
            rateioResumoTitulo: 'Resumo do rateio',
            rateioTotalDespesas: 'Total de despesas',
            rateioQtdPessoas: 'Pessoas envolvidas',
            rateioValorPorPessoa: 'Valor por pessoa',
            rateioListaTitulo: 'Divisão por pessoa',
            rateioVoce: 'Você (organizador)',
            rateioSemColaboradoresAtivos: 'Adicione colaboradores ativos para dividir os custos entre mais pessoas.',
            rateioAvisoSemDespesas: 'Adicione itens do catálogo a este evento para calcular o rateio automático.',

            convitePopupTitulo: 'Convite para colaborar',
            convitePopupTexto: 'Você foi convidado(a) para colaborar no evento "{evento}". Deseja aceitar?',
            botaoAceitarConvite: 'Aceitar convite',
            botaoRecusarConvite: 'Recusar',
            conviteAceitoToast: 'Convite aceito! Agora você é colaborador(a) deste evento.',
            conviteRecusadoToast: 'Convite recusado.',
            conviteInvalido: 'Esse convite não é mais válido ou já foi respondido.',

            notificacoesTitulo: 'Notificações',
            nenhumaNotificacao: 'Nenhuma notificação por enquanto.',
            notifConviteTexto: 'Você foi convidado(a) para colaborar no evento "{evento}"',
            notifBotaoAceitar: 'Aceitar',
            notifBotaoRecusar: 'Recusar',
            notifAceitaTag: 'Aceito ✓',
            notifRecusadaTag: 'Recusado',

            itensCompartilhadosTitulo: 'Lista compartilhada (junta-panelas)',
            itensCompartilhadosTexto: 'Combine com os colaboradores quem leva cada item — sem duplicar esforço.',
            labelNomeItemCompartilhado: 'Item',
            placeholderNomeItemCompartilhado: 'Ex: Refrigerante 2L',
            labelQtdItemCompartilhado: 'Quantidade',
            botaoAdicionarItemCompartilhado: 'Adicionar à lista',
            nenhumItemCompartilhado: 'Nenhum item na lista compartilhada ainda. Adicione o primeiro!',
            itemJaExisteAviso: '"{nome}" já está na lista — role até ele para marcar que vai levar.',
            itemSemResponsavel: 'Ninguém levando ainda',
            botaoEuVouLevar: 'Eu vou levar',
            botaoLiberarItem: 'Liberar item',
            levadoPor: 'Levando: {nome}',
            removerItemCompartilhadoAria: 'Remover item',
            escolherResponsavelTitulo: 'Quem vai levar "{item}"?',
            opcaoEuMesma: 'Eu (organizador)',
            semColaboradoresParaAssumir: 'Convide colaboradores para que eles também possam assumir itens.',
        },
        en: {
            nomeIdioma: 'English',
            navInicio: 'Home', navPlanejar: 'Plan event', navCatalogo: 'Catalog', navConfig: 'Settings', sair: 'Log out',
            contaPremium: 'Premium account',
            buscaTopoPlaceholder: 'Search events, vendors...',
            rodapeMarca: 'Momentus — moments planned with care',
            rodapeDireitos: '© 2026 Momentus. All rights reserved.',

            iniPainel: 'Dashboard',
            iniOla: 'Hi, {nome}!',
            iniSubtitulo0: 'No events yet. How about planning your first one?',
            iniSubtitulo1: 'You have 1 event coming up. Let\u2019s get everything ready to shine?',
            iniSubtituloN: 'You have {n} events coming up. Let\u2019s get everything ready to shine?',
            proximoEvento: 'Next event',
            ultimaAlteracao: 'Last updated {n} day(s) ago',
            criadoAgora: 'Created just now',
            preparativos: 'Preparations completed',
            semEventoTitulo: 'No events planned yet',
            semEventoTexto: 'Tap "Plan event" to create your first one and track everything here.',
            planejarEvento: 'Plan event',
            planejarDescZero: 'Start from scratch and build an unforgettable event',
            planejarDescModelo: 'Use a ready-made template and save time',
            chipCasamento: 'Wedding', chipCorporativo: 'Corporate', chipFormatura: 'Graduation',
            statEventosAtivos: 'Active events',
            statConvidados: 'Confirmed guests',
            statDias: 'Days to next event',
            statOrcamento: 'Budget reserved',
            calendario: 'Calendar',
            proximosEventos: 'Upcoming events',
            semProximos: 'No events scheduled yet.',
            statusConfirmado: 'Confirmed', statusPlanejamento: 'Planning', statusAgendado: 'Scheduled', statusRascunho: 'Draft',
            pesquisar: 'Search',
            buscaCatalogoPlaceholder: 'Snacks, cake, decoration...',

            planNovoEvento: 'New event',
            planTitulo: 'Let\u2019s plan your event',
            planSubtitulo: 'Fill in the details below — you can adjust everything later.',
            planTipoEvento: 'Event type',
            catAniversario: 'Birthday', catCasamento: 'Wedding', catChurrasco: 'BBQ', catFormatura: 'Graduation', catCorporativo: 'Corporate', catChaBebe: 'Baby shower',
            labelNomeEvento: 'Event name', placeholderNomeEvento: 'E.g.: Sofia\u2019s birthday',
            labelData: 'Date', labelHorario: 'Time', placeholderHorario: '3:00 PM',
            labelLocal: 'Location', placeholderLocal: 'Address or venue name',
            labelConvidados: 'Number of guests', placeholderConvidados: '50',
            labelEstilo: 'Style', estiloIntimista: 'Intimate', estiloClassico: 'Classic', estiloTematico: 'Themed', estiloArLivre: 'Outdoor',
            labelOrcamento: 'Estimated budget', ajudaOrcamento: '(drag to adjust)',
            labelObservacoes: 'Notes', placeholderObservacoes: 'Tell us a bit more about the mood you imagine for the event...',
            botaoSalvarEvento: 'Save event', botaoSalvarEventoOk: 'Event saved!',
            botaoRascunho: 'Save as draft', botaoRascunhoOk: 'Draft saved!',
            resumoTitulo: 'Event summary',
            resumoTipo: 'Type', resumoNome: 'Name', resumoData: 'Date', resumoConvidados: 'Guests', resumoOrcamento: 'Budget',
            resumoConvidadosSufixo: 'guests',
            checklistLocal: 'Choose the venue', checklistCardapio: 'Set the menu in the Catalog', checklistConvites: 'Send the invitations', checklistFornecedores: 'Confirm the vendors',

            catFornecedores: 'Vendors & products',
            catTitulo: 'Catalog',
            catSubtitulo: 'Everything you need to build the perfect event, in one place.',
            catBuscaPlaceholder: 'Search by business name...',
            filtroTodos: 'All', filtroSalgados: 'Savory', filtroDoces: 'Sweets', filtroBebidas: 'Drinks', filtroDecoracao: 'Decoration', filtroBuffet: 'Catering',

            confSuaConta: 'Your account',
            confTitulo: 'Settings',
            confSubtitulo: 'Adjust your profile, preferences and notifications.',
            confNomeCompleto: 'Full name', confEmail: 'Email', confTelefone: 'Phone',
            confSalvarAlteracoes: 'Save changes', confAlteracoesSalvas: 'Changes saved!',
            confNotificacoes: 'Notifications',
            confRsvpTitulo: 'Guest confirmations', confRsvpDesc: 'Get notified on every RSVP',
            confLembretesTitulo: 'Event reminders', confLembretesDesc: 'Alerts 48h before each event',
            confNovidadesTitulo: 'News and promotions', confNovidadesDesc: 'Offers from partner vendors',
            confPreferencias: 'Preferences',
            confTemaEscuro: 'Dark theme', confTemaEscuroDesc: 'Reduces interface brightness',
            confIdioma: 'Language', confIdiomaDesc: 'English',
            confPagamento: 'Account security', confPagamentoDesc: 'Protected session and data stored in the Momentus database', confAlterar: 'Change',
            confZonaRisco: 'Danger zone',
            confExcluirTitulo: 'Delete my account', confExcluirDesc: 'This action is permanent and cannot be undone', confExcluir: 'Delete',

            verTodosEventos: 'View all events',
            todosEventosEyebrow: 'Your events',
            todosEventosTitulo: 'All events',
            todosEventosSubtitulo: 'Track, edit or delete the events you have planned.',
            buscarEventosPlaceholder: 'Search by name, venue or type...',
            nenhumEventoCriadoTitulo: 'No events here yet',
            nenhumEventoCriadoTexto: 'Tap "Plan event" to create your first one.',
            botaoEditar: 'Edit',
            botaoApagar: 'Delete',
            confirmarApagarEvento: 'Are you sure you want to delete "{nome}"? This action cannot be undone.',
            cardEventoConvidados: 'guests',
            voltarEventos: 'Back',
            voltarInicio: 'Back to home',
            eventoNaoEncontradoTitulo: 'Event not found',
            eventoNaoEncontradoTexto: 'This event may have been deleted. See all your events.',
            abaInformacoes: 'Information',
            abaConvidados: 'Guests',
            abaItens: 'Catalog items',
            abaTarefas: 'Tasks',
            detalhesEvento: 'Event details',
            localDoEvento: 'Venue',
            dataEHora: 'Date and time',
            estiloDoEvento: 'Style',
            orcamentoEstimadoLabel: 'Estimated budget',
            orcamentoGastoLabel: 'Already reserved in the catalog',
            observacoesTitulo: 'Notes',
            semObservacoes: 'No notes recorded.',
            convidadosTitulo: 'Guest list',
            convidadosResumo: '{confirmados} confirmed · {pendentes} pending · {recusados} declined',
            nomeConvidadoLabel: 'Name',
            contatoConvidadoLabel: 'Contact (email or phone)',
            placeholderNomeConvidado: 'Guest name',
            placeholderContatoConvidado: 'email@example.com or (31) 90000-0000',
            botaoAdicionarConvidado: 'Add guest',
            nenhumConvidado: 'No guests added yet.',
            statusConvidadoPendente: 'Pending',
            statusConvidadoConfirmado: 'Confirmed',
            statusConvidadoRecusado: 'Declined',
            itensCatalogoTitulo: 'Catalog items',
            itensCatalogoTexto: 'Products and vendors added to this event.',
            nenhumItemCatalogo: 'No catalog items added yet. Visit the Catalog and use the "+" button.',
            irParaCatalogo: 'Go to catalog',
            tarefasTitulo: 'Task list',
            progressoPreparativos: 'Preparations completed',
            escolherEventoTitulo: 'Add to an event',
            escolherEventoTexto: 'Choose the event where you want to add "{produto}":',
            semEventosParaAdicionarTitulo: 'You don\u2019t have any events yet',
            semEventosParaAdicionarTexto: 'Create an event first so you can add catalog items to it.',
            criarEventoAgora: 'Create event now',
            itemAdicionadoEvento: 'Added to "{evento}"!',
            filtroFavoritos: 'Favorites ♥',
            nenhumFavorito: 'You haven\u2019t favorited anything yet. Tap the heart on a product to save it here.',
            fecharModal: 'Close',
            totalItensEvento: 'Total in items',
            removerItem: 'Remove',
            removerConvidadoAria: 'Remove guest',
            editarEventoTitulo: 'Edit event',
            salvarAlteracoesEvento: 'Save changes',
            alteracoesSalvasEvento: 'Changes saved!',
            verEvento: 'View event',

            abaColaboracao: 'Collaboration',
            colaboradoresTitulo: 'Event collaborators',
            colaboradoresTexto: 'Invite people to help organize and split up the items for this event.',
            botaoAdicionarColaborador: 'Add collaborator',
            nenhumColaborador: 'No collaborators added yet.',
            statusColabPendente: 'Invite pending',
            statusColabAtivo: 'Active collaborator',
            statusColabRecusado: 'Invite declined',
            modalColaboradorTitulo: 'Add collaborator',
            modalColaboradorTexto: 'Invite someone to help organize this event and split up the shared list items.',
            labelNomeColaborador: 'Name',
            placeholderNomeColaborador: 'Collaborator\u2019s name',
            labelEmailColaborador: 'Email',
            placeholderEmailColaborador: 'email@example.com',
            botaoEnviarConviteEmail: 'Send invite by email',
            botaoCopiarLinkConvite: 'Copy invite link',
            avisoLinkConvite: 'Share this link on WhatsApp, email, or wherever you like. Whoever opens it can accept the invite.',
            linkCopiado: 'Link copied! Now just share it.',
            linkNaoCopiado: 'Couldn\u2019t copy automatically. Copy it manually: {link}',
            conviteEnviadoEmail: 'Invite sent to {email}. They\u2019ll get a notification to accept it.',
            erroPreencherNomeColaborador: 'Enter the collaborator\u2019s name.',
            erroPreencherEmailColaborador: 'Enter an email to send the invite.',
            removerColaboradorAria: 'Remove collaborator',
            confirmarRemoverColaborador: 'Remove {nome} from the collaborators list?',
            reenviarConvite: 'Resend invite',
            conviteReenviado: 'Invite resent!',

            rateioTitulo: 'Expense splitting',
            rateioTexto: 'Split the event cost between you and your active collaborators.',
            rateioAtivarLabel: 'Enable splitting',
            rateioModoLabel: 'How to calculate the amount',
            rateioModoAuto: 'Automatic (based on total expenses)',
            rateioModoFixo: 'Fixed amount per person',
            labelValorFixoRateio: 'Fixed amount per person ($)',
            placeholderValorFixoRateio: 'E.g. 50.00',
            rateioResumoTitulo: 'Split summary',
            rateioTotalDespesas: 'Total expenses',
            rateioQtdPessoas: 'People involved',
            rateioValorPorPessoa: 'Amount per person',
            rateioListaTitulo: 'Split by person',
            rateioVoce: 'You (organizer)',
            rateioSemColaboradoresAtivos: 'Add active collaborators to split costs with more people.',
            rateioAvisoSemDespesas: 'Add catalog items to this event to calculate the automatic split.',

            convitePopupTitulo: 'Collaboration invite',
            convitePopupTexto: 'You\u2019ve been invited to collaborate on the event "{evento}". Do you want to accept?',
            botaoAceitarConvite: 'Accept invite',
            botaoRecusarConvite: 'Decline',
            conviteAceitoToast: 'Invite accepted! You\u2019re now a collaborator on this event.',
            conviteRecusadoToast: 'Invite declined.',
            conviteInvalido: 'This invite is no longer valid or was already answered.',

            notificacoesTitulo: 'Notifications',
            nenhumaNotificacao: 'No notifications yet.',
            notifConviteTexto: 'You\u2019ve been invited to collaborate on the event "{evento}"',
            notifBotaoAceitar: 'Accept',
            notifBotaoRecusar: 'Decline',
            notifAceitaTag: 'Accepted ✓',
            notifRecusadaTag: 'Declined',

            itensCompartilhadosTitulo: 'Shared list (potluck)',
            itensCompartilhadosTexto: 'Coordinate with collaborators who\u2019s bringing what — no duplicated effort.',
            labelNomeItemCompartilhado: 'Item',
            placeholderNomeItemCompartilhado: 'E.g.: 2L soda',
            labelQtdItemCompartilhado: 'Quantity',
            botaoAdicionarItemCompartilhado: 'Add to list',
            nenhumItemCompartilhado: 'No items on the shared list yet. Add the first one!',
            itemJaExisteAviso: '"{nome}" is already on the list — scroll to it to claim it.',
            itemSemResponsavel: 'No one bringing it yet',
            botaoEuVouLevar: 'I\u2019ll bring it',
            botaoLiberarItem: 'Release item',
            levadoPor: 'Bringing it: {nome}',
            removerItemCompartilhadoAria: 'Remove item',
            escolherResponsavelTitulo: 'Who\u2019s bringing "{item}"?',
            opcaoEuMesma: 'Me (organizer)',
            semColaboradoresParaAssumir: 'Invite collaborators so they can claim items too.',
        },
        es: {
            nomeIdioma: 'Español',
            navInicio: 'Inicio', navPlanejar: 'Planificar evento', navCatalogo: 'Catálogo', navConfig: 'Configuración', sair: 'Cerrar sesión',
            contaPremium: 'Cuenta Premium',
            buscaTopoPlaceholder: 'Buscar eventos, proveedores...',
            rodapeMarca: 'Momentus — momentos planeados con cariño',
            rodapeDireitos: '© 2026 Momentus. Todos los derechos reservados.',

            iniPainel: 'Panel de control',
            iniOla: '¡Hola, {nome}!',
            iniSubtitulo0: 'Aún no hay eventos. ¿Qué tal planificar el primero?',
            iniSubtitulo1: 'Tienes 1 evento acercándose. ¿Preparamos todo para que brille?',
            iniSubtituloN: 'Tienes {n} eventos acercándose. ¿Preparamos todo para que brille?',
            proximoEvento: 'Próximo evento',
            ultimaAlteracao: 'Última modificación hace {n} día(s)',
            criadoAgora: 'Creado hace un momento',
            preparativos: 'Preparativos completados',
            semEventoTitulo: 'Todavía no hay eventos planificados',
            semEventoTexto: 'Toca "Planificar evento" para crear el primero y seguir todo aquí.',
            planejarEvento: 'Planificar evento',
            planejarDescZero: 'Empieza desde cero y crea un evento inolvidable',
            planejarDescModelo: 'Usa una plantilla lista y ahorra tiempo',
            chipCasamento: 'Boda', chipCorporativo: 'Corporativo', chipFormatura: 'Graduación',
            statEventosAtivos: 'Eventos activos',
            statConvidados: 'Invitados confirmados',
            statDias: 'Días para el próximo evento',
            statOrcamento: 'Presupuesto reservado',
            calendario: 'Calendario',
            proximosEventos: 'Próximos eventos',
            semProximos: 'Aún no hay eventos programados.',
            statusConfirmado: 'Confirmado', statusPlanejamento: 'En planificación', statusAgendado: 'Programado', statusRascunho: 'Borrador',
            pesquisar: 'Buscar',
            buscaCatalogoPlaceholder: 'Bocadillos, pastel, decoración...',

            planNovoEvento: 'Nuevo evento',
            planTitulo: 'Vamos a planificar tu evento',
            planSubtitulo: 'Completa los datos a continuación — puedes ajustarlo todo después.',
            planTipoEvento: 'Tipo de evento',
            catAniversario: 'Cumpleaños', catCasamento: 'Boda', catChurrasco: 'Parrillada', catFormatura: 'Graduación', catCorporativo: 'Corporativo', catChaBebe: 'Baby shower',
            labelNomeEvento: 'Nombre del evento', placeholderNomeEvento: 'Ej.: Cumpleaños de Sofía',
            labelData: 'Fecha', labelHorario: 'Hora', placeholderHorario: '15:00',
            labelLocal: 'Lugar', placeholderLocal: 'Dirección o nombre del espacio',
            labelConvidados: 'Número de invitados', placeholderConvidados: '50',
            labelEstilo: 'Estilo', estiloIntimista: 'Íntimo', estiloClassico: 'Clásico', estiloTematico: 'Temático', estiloArLivre: 'Al aire libre',
            labelOrcamento: 'Presupuesto estimado', ajudaOrcamento: '(arrastra para ajustar)',
            labelObservacoes: 'Observaciones', placeholderObservacoes: 'Cuéntanos un poco más sobre el ambiente que imaginas para el evento...',
            botaoSalvarEvento: 'Guardar evento', botaoSalvarEventoOk: '¡Evento guardado!',
            botaoRascunho: 'Guardar como borrador', botaoRascunhoOk: '¡Borrador guardado!',
            resumoTitulo: 'Resumen del evento',
            resumoTipo: 'Tipo', resumoNome: 'Nombre', resumoData: 'Fecha', resumoConvidados: 'Invitados', resumoOrcamento: 'Presupuesto',
            resumoConvidadosSufixo: 'personas',
            checklistLocal: 'Elige el lugar', checklistCardapio: 'Define el menú en el Catálogo', checklistConvites: 'Envía las invitaciones', checklistFornecedores: 'Confirma los proveedores',

            catFornecedores: 'Proveedores y productos',
            catTitulo: 'Catálogo',
            catSubtitulo: 'Todo lo que necesitas para armar el evento perfecto, en un solo lugar.',
            catBuscaPlaceholder: 'Buscar por nombre del establecimiento...',
            filtroTodos: 'Todos', filtroSalgados: 'Salados', filtroDoces: 'Dulces', filtroBebidas: 'Bebidas', filtroDecoracao: 'Decoración', filtroBuffet: 'Buffet',

            confSuaConta: 'Tu cuenta',
            confTitulo: 'Configuración',
            confSubtitulo: 'Ajusta tu perfil, preferencias y notificaciones.',
            confNomeCompleto: 'Nombre completo', confEmail: 'Correo electrónico', confTelefone: 'Teléfono',
            confSalvarAlteracoes: 'Guardar cambios', confAlteracoesSalvas: '¡Cambios guardados!',
            confNotificacoes: 'Notificaciones',
            confRsvpTitulo: 'Confirmaciones de invitados', confRsvpDesc: 'Recibe un aviso en cada RSVP',
            confLembretesTitulo: 'Recordatorios de eventos', confLembretesDesc: 'Alertas 48h antes de cada evento',
            confNovidadesTitulo: 'Novedades y promociones', confNovidadesDesc: 'Ofertas de proveedores asociados',
            confPreferencias: 'Preferencias',
            confTemaEscuro: 'Tema oscuro', confTemaEscuroDesc: 'Reduce el brillo de la interfaz',
            confIdioma: 'Idioma', confIdiomaDesc: 'Español',
            confPagamento: 'Seguridad de la cuenta', confPagamentoDesc: 'Sesión protegida y datos guardados en la base de Momentus', confAlterar: 'Cambiar',
            confZonaRisco: 'Zona de riesgo',
            confExcluirTitulo: 'Eliminar mi cuenta', confExcluirDesc: 'Esta acción es permanente y no se puede deshacer', confExcluir: 'Eliminar',

            verTodosEventos: 'Ver todos los eventos',
            todosEventosEyebrow: 'Tus eventos',
            todosEventosTitulo: 'Todos los eventos',
            todosEventosSubtitulo: 'Sigue, edita o elimina los eventos que ya planificaste.',
            buscarEventosPlaceholder: 'Buscar por nombre, lugar o tipo...',
            nenhumEventoCriadoTitulo: 'Todavía no hay eventos aquí',
            nenhumEventoCriadoTexto: 'Toca "Planificar evento" para crear el primero.',
            botaoEditar: 'Editar',
            botaoApagar: 'Eliminar',
            confirmarApagarEvento: '¿Seguro que deseas eliminar "{nome}"? Esta acción no se puede deshacer.',
            cardEventoConvidados: 'invitados',
            voltarEventos: 'Volver',
            voltarInicio: 'Volver al inicio',
            eventoNaoEncontradoTitulo: 'Evento no encontrado',
            eventoNaoEncontradoTexto: 'Este evento pudo haber sido eliminado. Mira todos tus eventos.',
            abaInformacoes: 'Información',
            abaConvidados: 'Invitados',
            abaItens: 'Artículos del catálogo',
            abaTarefas: 'Tareas',
            detalhesEvento: 'Detalles del evento',
            localDoEvento: 'Lugar',
            dataEHora: 'Fecha y hora',
            estiloDoEvento: 'Estilo',
            orcamentoEstimadoLabel: 'Presupuesto estimado',
            orcamentoGastoLabel: 'Ya reservado en el catálogo',
            observacoesTitulo: 'Observaciones',
            semObservacoes: 'Ninguna observación registrada.',
            convidadosTitulo: 'Lista de invitados',
            convidadosResumo: '{confirmados} confirmados · {pendentes} pendientes · {recusados} rechazaron',
            nomeConvidadoLabel: 'Nombre',
            contatoConvidadoLabel: 'Contacto (correo o teléfono)',
            placeholderNomeConvidado: 'Nombre del invitado',
            placeholderContatoConvidado: 'email@ejemplo.com o (31) 90000-0000',
            botaoAdicionarConvidado: 'Agregar invitado',
            nenhumConvidado: 'Todavía no hay invitados agregados.',
            statusConvidadoPendente: 'Pendiente',
            statusConvidadoConfirmado: 'Confirmado',
            statusConvidadoRecusado: 'Rechazó',
            itensCatalogoTitulo: 'Artículos del catálogo',
            itensCatalogoTexto: 'Productos y proveedores agregados a este evento.',
            nenhumItemCatalogo: 'Todavía no hay artículos del catálogo agregados. Visita el Catálogo y usa el botón "+".',
            irParaCatalogo: 'Ir al catálogo',
            tarefasTitulo: 'Lista de tareas',
            progressoPreparativos: 'Preparativos completados',
            escolherEventoTitulo: 'Agregar a un evento',
            escolherEventoTexto: 'Elige el evento donde deseas incluir "{produto}":',
            semEventosParaAdicionarTitulo: 'Todavía no tienes eventos',
            semEventosParaAdicionarTexto: 'Crea un evento primero para poder agregarle artículos del catálogo.',
            criarEventoAgora: 'Crear evento ahora',
            itemAdicionadoEvento: '¡Agregado a "{evento}"!',
            filtroFavoritos: 'Favoritos ♥',
            nenhumFavorito: 'Todavía no has marcado nada como favorito. Toca el corazón de un producto para guardarlo aquí.',
            fecharModal: 'Cerrar',
            totalItensEvento: 'Total en artículos',
            removerItem: 'Quitar',
            removerConvidadoAria: 'Quitar invitado',
            editarEventoTitulo: 'Editar evento',
            salvarAlteracoesEvento: 'Guardar cambios',
            alteracoesSalvasEvento: '¡Cambios guardados!',
            verEvento: 'Ver evento',

            abaColaboracao: 'Colaboración',
            colaboradoresTitulo: 'Colaboradores del evento',
            colaboradoresTexto: 'Invita a personas para ayudar a organizar y repartir los artículos de este evento.',
            botaoAdicionarColaborador: 'Agregar colaborador',
            nenhumColaborador: 'Todavía no hay colaboradores agregados.',
            statusColabPendente: 'Invitación pendiente',
            statusColabAtivo: 'Colaborador activo',
            statusColabRecusado: 'Invitación rechazada',
            modalColaboradorTitulo: 'Agregar colaborador',
            modalColaboradorTexto: 'Invita a alguien para ayudar a organizar este evento y repartir los artículos de la lista compartida.',
            labelNomeColaborador: 'Nombre',
            placeholderNomeColaborador: 'Nombre del colaborador',
            labelEmailColaborador: 'Correo electrónico',
            placeholderEmailColaborador: 'correo@ejemplo.com',
            botaoEnviarConviteEmail: 'Enviar invitación por correo',
            botaoCopiarLinkConvite: 'Copiar enlace de invitación',
            avisoLinkConvite: 'Comparte este enlace por WhatsApp, correo o donde prefieras. Quien lo abra podrá aceptar la invitación.',
            linkCopiado: '¡Enlace copiado! Ahora solo compártelo.',
            linkNaoCopiado: 'No se pudo copiar automáticamente. Copia manualmente: {link}',
            conviteEnviadoEmail: 'Invitación enviada a {email}. Esa persona recibirá un aviso para aceptarla.',
            erroPreencherNomeColaborador: 'Escribe el nombre del colaborador.',
            erroPreencherEmailColaborador: 'Escribe un correo para enviar la invitación.',
            removerColaboradorAria: 'Quitar colaborador',
            confirmarRemoverColaborador: '¿Quitar a {nome} de la lista de colaboradores?',
            reenviarConvite: 'Reenviar invitación',
            conviteReenviado: '¡Invitación reenviada!',

            rateioTitulo: 'Reparto de gastos',
            rateioTexto: 'Divide el costo del evento entre tú y los colaboradores activos.',
            rateioAtivarLabel: 'Activar reparto',
            rateioModoLabel: 'Cómo calcular el valor',
            rateioModoAuto: 'Automático (según los gastos totales)',
            rateioModoFixo: 'Valor fijo por persona',
            labelValorFixoRateio: 'Valor fijo por persona ($)',
            placeholderValorFixoRateio: 'Ej: 50,00',
            rateioResumoTitulo: 'Resumen del reparto',
            rateioTotalDespesas: 'Total de gastos',
            rateioQtdPessoas: 'Personas involucradas',
            rateioValorPorPessoa: 'Valor por persona',
            rateioListaTitulo: 'Reparto por persona',
            rateioVoce: 'Tú (organizador)',
            rateioSemColaboradoresAtivos: 'Agrega colaboradores activos para repartir los gastos entre más personas.',
            rateioAvisoSemDespesas: 'Agrega artículos del catálogo a este evento para calcular el reparto automático.',

            convitePopupTitulo: 'Invitación para colaborar',
            convitePopupTexto: 'Fuiste invitado(a) a colaborar en el evento "{evento}". ¿Deseas aceptar?',
            botaoAceitarConvite: 'Aceptar invitación',
            botaoRecusarConvite: 'Rechazar',
            conviteAceitoToast: '¡Invitación aceptada! Ahora eres colaborador(a) de este evento.',
            conviteRecusadoToast: 'Invitación rechazada.',
            conviteInvalido: 'Esta invitación ya no es válida o ya fue respondida.',

            notificacoesTitulo: 'Notificaciones',
            nenhumaNotificacao: 'Todavía no hay notificaciones.',
            notifConviteTexto: 'Fuiste invitado(a) a colaborar en el evento "{evento}"',
            notifBotaoAceitar: 'Aceptar',
            notifBotaoRecusar: 'Rechazar',
            notifAceitaTag: 'Aceptado ✓',
            notifRecusadaTag: 'Rechazado',

            itensCompartilhadosTitulo: 'Lista compartida (entre todos)',
            itensCompartilhadosTexto: 'Coordina con los colaboradores quién lleva cada cosa, sin duplicar esfuerzos.',
            labelNomeItemCompartilhado: 'Artículo',
            placeholderNomeItemCompartilhado: 'Ej.: Refresco 2L',
            labelQtdItemCompartilhado: 'Cantidad',
            botaoAdicionarItemCompartilhado: 'Agregar a la lista',
            nenhumItemCompartilhado: 'Todavía no hay artículos en la lista compartida. ¡Agrega el primero!',
            itemJaExisteAviso: '"{nome}" ya está en la lista — desplázate hasta él para marcar que lo llevarás.',
            itemSemResponsavel: 'Nadie lo está llevando todavía',
            botaoEuVouLevar: 'Yo lo llevo',
            botaoLiberarItem: 'Liberar artículo',
            levadoPor: 'Lo lleva: {nome}',
            removerItemCompartilhadoAria: 'Quitar artículo',
            escolherResponsavelTitulo: '¿Quién va a llevar "{item}"?',
            opcaoEuMesma: 'Yo (organizador)',
            semColaboradoresParaAssumir: 'Invita colaboradores para que ellos también puedan asumir artículos.',
        }
    };

    const MESES = {
        pt: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        es: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    };
    const MESES_ABREV = {
        pt: ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ'],
        en: ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'],
        es: ['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC']
    };
    const SEMANA_CURTA = {
        pt: ['Do', 'Se', 'Te', 'Qa', 'Qi', 'Se', 'Sa'],
        en: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
        es: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa']
    };

    function obterMeses() { return MESES[obterIdioma()] || MESES.pt; }
    function obterMesesAbrev() { return MESES_ABREV[obterIdioma()] || MESES_ABREV.pt; }
    function obterSemanaCurta() { return SEMANA_CURTA[obterIdioma()] || SEMANA_CURTA.pt; }

    function obterIdioma() {
        return localStorage.getItem(CHAVE_IDIOMA) || 'pt';
    }

    function t(chave, params) {
        const dic = IDIOMAS[obterIdioma()] || IDIOMAS.pt;
        let texto = dic[chave] !== undefined ? dic[chave] : (IDIOMAS.pt[chave] || chave);
        if (params) {
            Object.keys(params).forEach((p) => {
                texto = texto.replace(`{${p}}`, params[p]);
            });
        }
        return texto;
    }

    function aplicarIdioma(idioma, notificar) {
        if (notificar === undefined) notificar = true;
        if (!IDIOMAS[idioma]) idioma = 'pt';
        localStorage.setItem(CHAVE_IDIOMA, idioma);
        document.documentElement.setAttribute('lang', idioma === 'pt' ? 'pt-br' : idioma);

        document.querySelectorAll('[data-i18n]').forEach((el) => {
            const chave = el.getAttribute('data-i18n');
            el.textContent = t(chave);
        });
        document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
            el.setAttribute('placeholder', t(el.getAttribute('data-i18n-placeholder')));
        });
        document.querySelectorAll('[data-i18n-aria]').forEach((el) => {
            el.setAttribute('aria-label', t(el.getAttribute('data-i18n-aria')));
        });
        document.querySelectorAll('select[data-controle-idioma]').forEach((sel) => {
            sel.value = idioma;
        });

        const cabecalhoSemana = document.querySelectorAll('.calendario-topo span');
        if (cabecalhoSemana.length === 7) {
            obterSemanaCurta().forEach((dia, i) => { cabecalhoSemana[i].textContent = dia; });
        }

        if (notificar) {
            document.dispatchEvent(new CustomEvent('momentus:idioma-alterado'));
        }
    }

    /* ================= PERFIL / SESSÃO ================= */

    let _perfilCache = { nome: 'Usuário', email: '', telefone: '', tipo: 'cliente' };
    let _sessaoResolvida = false;
    let _resolverSessao;
    const _sessaoPronta = new Promise((resolve) => { _resolverSessao = resolve; });

    function paginaPublica() {
        const nome = (location.pathname.split('/').pop() || '').toLowerCase();
        return ['', 'index.html', 'cadastro.html', 'rsvp.html', 'convite.html'].includes(nome);
    }

    function redirecionarLogin() {
        if (!paginaPublica()) {
            const destino = encodeURIComponent(location.pathname.split('/').pop() + location.search);
            window.location.href = 'index.html?next=' + destino;
        }
    }

    async function sincronizarPerfil() {
        try {
            const resposta = await MomentusAPI.me();
            _perfilCache = resposta.usuario || _perfilCache;
            aplicarPerfilNaTela();
            document.dispatchEvent(new CustomEvent('momentus:perfil-alterado'));
        } catch (erro) {
            if (erro.status === 401) redirecionarLogin();
        } finally {
            _sessaoResolvida = true;
            _resolverSessao();
        }
    }

    function aguardarSessaoPronta() { return _sessaoPronta; }

    function obterPerfil() {
        return Object.assign({}, _perfilCache);
    }

    async function salvarPerfil(perfil) {
        try {
            const resposta = await MomentusAPI.atualizarPerfil(perfil);
            _perfilCache = resposta.usuario || _perfilCache;
            aplicarPerfilNaTela();
            document.dispatchEvent(new CustomEvent('momentus:perfil-alterado'));
            return _perfilCache;
        } catch (erro) {
            avisarErro(erro, 'Não foi possível salvar seu perfil.');
            return null;
        }
    }

    function iniciais(nome) {
        return String(nome || '').split(' ').filter(Boolean).slice(0, 2).map((p) => p[0].toUpperCase()).join('') || 'M';
    }

    function aplicarPerfilNaTela() {
        const perfil = obterPerfil();
        document.querySelectorAll('.perfilNome').forEach((el) => { el.textContent = perfil.nome || 'Usuário'; });
        document.querySelectorAll('.avatarPerfil, .avatarTopo').forEach((el) => { el.textContent = iniciais(perfil.nome); });
        document.querySelectorAll('.perfilTag').forEach((el) => {
            el.textContent = 'Organizador(a)';
        });
        document.querySelectorAll('.avatarGrande').forEach((el) => {
            if (el.firstChild && el.firstChild.nodeType === 3) el.firstChild.textContent = iniciais(perfil.nome) + ' ';
        });
        const primeiroNome = String(perfil.nome || 'Usuário').split(' ')[0];
        document.querySelectorAll('[data-nome-usuario]').forEach((el) => { el.textContent = primeiroNome; });
    }

    async function sair() {
        try { await MomentusAPI.logout(); } catch (_) { /* ignora */ }
        window.location.href = 'index.html';
    }

    async function excluirConta() {
        try {
            await MomentusAPI.excluirConta();
            window.location.href = 'index.html';
            return true;
        } catch (erro) { avisarErro(erro, 'Não foi possível excluir a conta.'); return false; }
    }

    /* ================= PREFERÊNCIAS (somente interface) ================= */

    function obterPreferencias() {
        try {
            const p = JSON.parse(localStorage.getItem(CHAVE_PREFS));
            if (p) return p;
        } catch (e) { /* ignora */ }
        return { rsvp: true, lembretes: true, novidades: false };
    }

    function salvarPreferencias(prefs) {
        // Preferências de interruptores de interface podem ficar no navegador.
        localStorage.setItem(CHAVE_PREFS, JSON.stringify(prefs));
    }

    /* ================= EVENTOS (banco via API) ================= */

    function tarefasPadrao() {
        return [
            { id: 't1', chave: 'checklistLocal', titulo: 'Escolha o local', feita: false },
            { id: 't2', chave: 'checklistCardapio', titulo: 'Defina o cardápio', feita: false },
            { id: 't3', chave: 'checklistConvites', titulo: 'Envie os convites', feita: false },
            { id: 't4', chave: 'checklistFornecedores', titulo: 'Confirme os fornecedores', feita: false }
        ];
    }

    function eventoParaPayloadAPI(evento) {
        return {
            nome_evento: (evento.nome || evento.tipoLabel || 'Evento').toString(),
            tipo_evento: (evento.tipo || 'evento').toString(),
            data_evento: evento.data,
            hora_evento: evento.hora && evento.hora !== '—' ? evento.hora : '',
            endereco_evento: evento.local || '',
            cidade_evento: evento.cidade || '',
            orcamento_evento: Number(evento.orcamento) || 0,
            convidados_estimados: Number(evento.convidados) || 0,
            estilo_evento: evento.estilo || '',
            observacoes: evento.observacoes || '',
            status: evento.status || 'agendado',
            progresso: Number(evento.progresso) || 0,
            privacidade_convidados: evento.privacidadeConvidados || 'organizador',
            rateio: evento.rateio || undefined
        };
    }

    function eventoDaAPI(registro) {
        return {
            id: String(registro.id),
            ownerId: registro.owner_id ? String(registro.owner_id) : null,
            owner: registro.owner || null,
            permissao: registro.permissao || (registro.owner_id === _perfilCache.id ? 'dono' : 'colaborador'),
            podeEditar: registro.pode_editar !== false,
            tipo: registro.tipo_evento,
            tipoLabel: registro.tipo_evento,
            nome: registro.nome_evento,
            data: registro.data_evento,
            hora: registro.hora_evento || '—',
            local: registro.endereco_evento || '',
            cidade: registro.cidade_evento || '',
            orcamento: Number(registro.orcamento_evento) || 0,
            convidados: Number(registro.convidados_estimados) || 0,
            estilo: registro.estilo_evento || '',
            observacoes: registro.observacoes || '',
            status: registro.status || 'agendado',
            progresso: Number(registro.progresso) || 0,
            privacidadeConvidados: registro.privacidade_convidados || 'organizador',
            criadoEm: registro.criado_em || (registro.data_evento + 'T00:00:00'),
            listaConvidados: registro.lista_convidados || [],
            itensCatalogo: registro.itens_catalogo || [],
            tarefas: registro.tarefas || [],
            colaboradores: registro.colaboradores || [],
            itensCompartilhados: registro.itens_compartilhados || [],
            despesas: registro.despesas || [],
            fotos: registro.fotos || [],
            rateio: registro.rateio || { ativo: false, modo: 'auto', valorFixo: 0 },
            totalDespesas: Number(registro.total_despesas) || 0,
            confirmados: Number(registro.confirmados) || 0
        };
    }

    let _eventosCache = [];
    let _resolverEventosProntos;
    const _eventosProntos = new Promise((resolve) => { _resolverEventosProntos = resolve; });
    let _primeiraSincronizacao = true;

    function avisarErro(erro, mensagemPadrao) {
        console.error('Momentus:', erro);
        const texto = (erro && erro.message) || mensagemPadrao;
        if (typeof window.mostrarToast === 'function') window.mostrarToast(texto, 'erro');
    }

    async function sincronizarEventos() {
        try {
            const registros = await MomentusAPI.listarEventos();
            _eventosCache = (registros || []).map(eventoDaAPI);
        } catch (erro) {
            if (erro.status === 401) redirecionarLogin();
            else avisarErro(erro, 'Não foi possível carregar os eventos do servidor.');
        } finally {
            document.dispatchEvent(new CustomEvent('momentus:eventos-alterados'));
            if (_primeiraSincronizacao) {
                _primeiraSincronizacao = false;
                _resolverEventosProntos();
            }
        }
    }

    function aguardarEventosProntos() { return _eventosProntos; }
    function obterEventos() { return _eventosCache.slice(); }
    function obterEvento(id) { return _eventosCache.find((ev) => String(ev.id) === String(id)) || null; }

    async function salvarEvento(evento) {
        try {
            const criado = await MomentusAPI.criarEvento(eventoParaPayloadAPI(evento));
            await sincronizarEventos();
            return obterEvento(criado.id) || eventoDaAPI(criado);
        } catch (erro) {
            avisarErro(erro, 'Não foi possível salvar o evento.');
            return null;
        }
    }

    async function removerEvento(id) {
        try {
            await MomentusAPI.removerEvento(id);
            await sincronizarEventos();
            return true;
        } catch (erro) {
            avisarErro(erro, 'Não foi possível remover o evento.');
            return false;
        }
    }

    function diasEntre(dataISO) {
        const hoje = new Date();
        hoje.setHours(0, 0, 0, 0);
        const alvo = new Date(dataISO + 'T00:00:00');
        return Math.round((alvo - hoje) / 86400000);
    }

    async function atualizarEvento(id, dadosNovos) {
        const atual = obterEvento(id);
        if (!atual) return null;
        const mesclado = Object.assign({}, atual, dadosNovos);
        try {
            const registro = await MomentusAPI.atualizarEvento(id, eventoParaPayloadAPI(mesclado));
            await sincronizarEventos();
            return obterEvento(id) || eventoDaAPI(registro);
        } catch (erro) {
            avisarErro(erro, 'Não foi possível salvar as alterações.');
            return null;
        }
    }

    /* ---- Convidados: pessoas convidadas NÃO viram colaboradoras ---- */

    async function adicionarConvidado(eventoId, convidado) {
        try {
            const criado = await MomentusAPI.adicionarConvidado(eventoId, convidado);
            await sincronizarEventos();
            return criado;
        } catch (erro) {
            avisarErro(erro, 'Não foi possível adicionar o convidado.');
            return null;
        }
    }

    async function removerConvidado(eventoId, convidadoId) {
        try {
            await MomentusAPI.removerConvidado(eventoId, convidadoId);
            await sincronizarEventos();
            return true;
        } catch (erro) { avisarErro(erro, 'Não foi possível remover o convidado.'); return false; }
    }

    async function definirStatusConvidado(eventoId, convidadoId, status) {
        try {
            await MomentusAPI.atualizarConvidado(eventoId, convidadoId, { status });
            await sincronizarEventos();
            return true;
        } catch (erro) { avisarErro(erro, 'Não foi possível atualizar o RSVP.'); return false; }
    }

    /* ---- Itens do catálogo por evento ---- */

    async function adicionarItemCatalogo(eventoId, item) {
        try {
            const criado = await MomentusAPI.adicionarItemEvento(eventoId, item);
            await sincronizarEventos();
            return criado;
        } catch (erro) { avisarErro(erro, 'Não foi possível adicionar o item.'); return null; }
    }

    async function removerItemCatalogo(eventoId, itemId) {
        try {
            await MomentusAPI.removerItemEvento(eventoId, itemId);
            await sincronizarEventos();
            return true;
        } catch (erro) { avisarErro(erro, 'Não foi possível remover o item.'); return false; }
    }

    /* ---- Notificações no banco ---- */

    let _notificacoesCache = [];
    async function sincronizarNotificacoes() {
        try {
            _notificacoesCache = await MomentusAPI.notificacoes() || [];
            document.dispatchEvent(new CustomEvent('momentus:notificacoes-alteradas'));
        } catch (erro) {
            if (erro.status !== 401) console.warn(erro);
        }
        return _notificacoesCache;
    }
    function obterNotificacoes() { return _notificacoesCache.slice(); }
    async function marcarNotificacoesLidas() {
        try {
            await MomentusAPI.marcarNotificacoesLidas();
            _notificacoesCache = _notificacoesCache.map((n) => Object.assign({}, n, { lida: true }));
            document.dispatchEvent(new CustomEvent('momentus:notificacoes-alteradas'));
        } catch (_) { /* ignora */ }
    }
    function marcarNotificacaoRespondida() { return true; }

    /* ---- Colaboradores ---- */

    function obterColaboradores(eventoId) {
        const evento = obterEvento(eventoId);
        return evento ? (evento.colaboradores || []) : [];
    }

    async function adicionarColaborador(eventoId, dados) {
        try {
            const criado = await MomentusAPI.adicionarColaborador(eventoId, { nome: dados.nome, email: dados.email || dados.contato });
            await sincronizarEventos();
            return criado;
        } catch (erro) { avisarErro(erro, 'Não foi possível convidar o colaborador.'); return null; }
    }

    function reenviarConviteColaborador(eventoId, colaboradorId) {
        const colab = obterColaboradores(eventoId).find((c) => String(c.id) === String(colaboradorId));
        return colab || null;
    }

    function obterConvitePorToken(token) {
        for (const evento of obterEventos()) {
            const colaborador = (evento.colaboradores || []).find((c) => c.token === token);
            if (colaborador) return { evento, colaborador };
        }
        return null;
    }

    async function responderColaborador(eventoId, colaboradorId, status) {
        const evento = obterEvento(eventoId);
        const colab = evento && (evento.colaboradores || []).find((c) => String(c.id) === String(colaboradorId));
        try {
            if (colab && colab.token && (status === 'ativo' || status === 'recusado')) {
                await MomentusAPI.responderConviteColaborador(colab.token, status);
            } else {
                await MomentusAPI.atualizarColaborador(eventoId, colaboradorId, { status });
            }
            await Promise.all([sincronizarEventos(), sincronizarNotificacoes()]);
            return true;
        } catch (erro) { avisarErro(erro, 'Não foi possível responder ao convite.'); return false; }
    }

    async function definirPermissaoColaborador(eventoId, colaboradorId, podeEditar) {
        try {
            await MomentusAPI.atualizarColaborador(eventoId, colaboradorId, { pode_editar: !!podeEditar });
            await sincronizarEventos();
            return true;
        } catch (erro) { avisarErro(erro, 'Não foi possível alterar a permissão.'); return false; }
    }

    async function removerColaborador(eventoId, colaboradorId) {
        try {
            await MomentusAPI.removerColaborador(eventoId, colaboradorId);
            await sincronizarEventos();
            return true;
        } catch (erro) { avisarErro(erro, 'Não foi possível remover o colaborador.'); return false; }
    }

    /* ---- Rateio de despesas ---- */

    function obterRateio(eventoId) {
        const evento = obterEvento(eventoId);
        return evento ? Object.assign({ ativo: false, modo: 'auto', valorFixo: 0 }, evento.rateio || {}) : { ativo: false, modo: 'auto', valorFixo: 0 };
    }

    async function definirRateio(eventoId, dados) {
        try {
            await MomentusAPI.definirRateio(eventoId, dados);
            await sincronizarEventos();
            return obterRateio(eventoId);
        } catch (erro) { avisarErro(erro, 'Não foi possível atualizar o rateio.'); return null; }
    }

    function calcularRateio(eventoId) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const rateio = obterRateio(eventoId);
        const totalDespesasRegistradas = (evento.despesas || []).reduce((s, d) => s + Number(d.valor || 0), 0);
        const totalItens = (evento.itensCatalogo || []).reduce((s, i) => s + Number(i.preco || 0) * Number(i.qtd || 1), 0);
        const totalDespesas = totalDespesasRegistradas + totalItens;
        const colaboradoresAtivos = (evento.colaboradores || []).filter((c) => c.status === 'ativo');
        const qtdPessoas = 1 + colaboradoresAtivos.length;
        const valorPorPessoa = rateio.modo === 'fixo' ? Number(rateio.valorFixo || 0) : (qtdPessoas ? totalDespesas / qtdPessoas : 0);
        const pessoas = [{ id: 'organizador', nome: obterPerfil().nome, valor: valorPorPessoa, organizador: true }]
            .concat(colaboradoresAtivos.map((c) => ({ id: c.id, nome: c.nome, valor: valorPorPessoa, organizador: false })));
        return { ativo: !!rateio.ativo, modo: rateio.modo, valorFixo: Number(rateio.valorFixo || 0), totalDespesas, qtdPessoas, valorPorPessoa, totalArrecadado: valorPorPessoa * qtdPessoas, pessoas };
    }

    /* ---- Lista compartilhada ---- */

    function obterItensCompartilhados(eventoId) {
        const evento = obterEvento(eventoId);
        return evento ? (evento.itensCompartilhados || []) : [];
    }

    async function adicionarItemCompartilhado(eventoId, dados) {
        try {
            const item = await MomentusAPI.adicionarItemCompartilhado(eventoId, dados);
            await sincronizarEventos();
            return { duplicado: false, item };
        } catch (erro) {
            if (erro.status === 409 && erro.corpo && erro.corpo.item) return { duplicado: true, item: erro.corpo.item };
            avisarErro(erro, 'Não foi possível adicionar o item compartilhado.');
            return null;
        }
    }

    async function assumirItemCompartilhado(eventoId, itemId, responsavel) {
        try {
            await MomentusAPI.atualizarItemCompartilhado(eventoId, itemId, responsavel);
            await sincronizarEventos();
            return true;
        } catch (erro) { avisarErro(erro, 'Não foi possível definir o responsável.'); return false; }
    }

    function liberarItemCompartilhado(eventoId, itemId) {
        return assumirItemCompartilhado(eventoId, itemId, { liberar: true });
    }

    async function removerItemCompartilhado(eventoId, itemId) {
        try {
            await MomentusAPI.removerItemCompartilhado(eventoId, itemId);
            await sincronizarEventos();
            return true;
        } catch (erro) { avisarErro(erro, 'Não foi possível remover o item.'); return false; }
    }

    /* ---- Tarefas ---- */

    async function alternarTarefa(eventoId, tarefaId) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const tarefa = (evento.tarefas || []).find((t) => String(t.id) === String(tarefaId));
        if (!tarefa) return null;
        try {
            await MomentusAPI.atualizarTarefa(eventoId, tarefaId, { feita: !tarefa.feita });
            await sincronizarEventos();
            return true;
        } catch (erro) { avisarErro(erro, 'Não foi possível atualizar a tarefa.'); return false; }
    }


    async function adicionarTarefa(eventoId, dados) {
        try { const r = await MomentusAPI.adicionarTarefa(eventoId, dados); await sincronizarEventos(); return r; }
        catch (erro) { avisarErro(erro, 'Não foi possível adicionar a tarefa.'); return null; }
    }

    async function removerTarefa(eventoId, tarefaId) {
        try { await MomentusAPI.removerTarefa(eventoId, tarefaId); await sincronizarEventos(); return true; }
        catch (erro) { avisarErro(erro, 'Não foi possível remover a tarefa.'); return false; }
    }

    /* ---- Favoritos no banco ---- */

    let _favoritosCache = [];
    async function sincronizarFavoritos() {
        try {
            _favoritosCache = await MomentusAPI.favoritos() || [];
            document.dispatchEvent(new CustomEvent('momentus:favoritos-alterados'));
        } catch (erro) { if (erro.status !== 401) console.warn(erro); }
        return _favoritosCache;
    }
    function obterFavoritos() { return _favoritosCache.slice(); }
    function ehFavorito(produtoId) { return _favoritosCache.includes(produtoId); }
    async function alternarFavorito(produtoId) {
        try {
            await MomentusAPI.alternarFavorito(produtoId);
            await sincronizarFavoritos();
            return obterFavoritos();
        } catch (erro) { avisarErro(erro, 'Não foi possível favoritar.'); return obterFavoritos(); }
    }

    /* ---- Finanças e galeria ---- */

    async function adicionarDespesa(eventoId, dados) {
        try { const r = await MomentusAPI.adicionarDespesa(eventoId, dados); await sincronizarEventos(); return r; }
        catch (erro) { avisarErro(erro, 'Não foi possível registrar a despesa.'); return null; }
    }
    async function removerDespesa(eventoId, despesaId) {
        try { await MomentusAPI.removerDespesa(eventoId, despesaId); await sincronizarEventos(); return true; }
        catch (erro) { avisarErro(erro, 'Não foi possível remover a despesa.'); return false; }
    }
    async function enviarComprovanteDespesa(eventoId, despesaId, arquivo) {
        try {
            const fd = new FormData(); fd.append('comprovante', arquivo);
            const r = await MomentusAPI.enviarComprovanteDespesa(eventoId, despesaId, fd);
            await sincronizarEventos(); return r;
        } catch (erro) { avisarErro(erro, 'Não foi possível enviar o comprovante.'); return null; }
    }
    async function obterResumoEvento(eventoId) {
        try { return await MomentusAPI.resumoEvento(eventoId); }
        catch (erro) { avisarErro(erro, 'Não foi possível carregar o resumo inteligente.'); return null; }
    }
    async function enviarFoto(eventoId, arquivo, legenda) {
        try {
            const fd = new FormData(); fd.append('foto', arquivo); fd.append('legenda', legenda || '');
            const r = await MomentusAPI.enviarFoto(eventoId, fd); await sincronizarEventos(); return r;
        } catch (erro) { avisarErro(erro, 'Não foi possível enviar a foto.'); return null; }
    }
    async function removerFoto(eventoId, fotoId) {
        try { await MomentusAPI.removerFoto(eventoId, fotoId); await sincronizarEventos(); return true; }
        catch (erro) { avisarErro(erro, 'Não foi possível remover a foto.'); return false; }
    }

    /* ================= INIT ================= */

    function iniciar() {
        aplicarTema(obterTema());
        aplicarIdioma(obterIdioma());
        aplicarPerfilNaTela();

        document.querySelectorAll('[data-controle-tema]').forEach((input) => {
            input.checked = obterTema() === 'escuro';
            input.addEventListener('change', () => aplicarTema(input.checked ? 'escuro' : 'claro'));
        });
        document.querySelectorAll('select[data-controle-idioma]').forEach((sel) => {
            sel.value = obterIdioma();
            sel.addEventListener('change', () => aplicarIdioma(sel.value));
        });
        document.querySelectorAll('.linkSair').forEach((link) => {
            link.addEventListener('click', (e) => { e.preventDefault(); sair(); });
        });
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
    else iniciar();

    // A sessão é carregada antes dos dados privados; nada de token/perfil no localStorage.
    sincronizarPerfil().then(() => {
        if (!paginaPublica()) {
            sincronizarEventos();
            sincronizarNotificacoes();
            sincronizarFavoritos();
        } else if (_sessaoResolvida && _perfilCache.email) {
            sincronizarNotificacoes();
        } else if (_primeiraSincronizacao) {
            _primeiraSincronizacao = false;
            _resolverEventosProntos();
        }
    });

    return {
        t, obterIdioma, aplicarIdioma, obterMeses, obterMesesAbrev, obterSemanaCurta,
        obterTema, aplicarTema, alternarTema,
        obterPerfil, salvarPerfil, iniciais, aplicarPerfilNaTela, aguardarSessaoPronta, sair, excluirConta,
        obterPreferencias, salvarPreferencias,
        obterEventos, salvarEvento, removerEvento, diasEntre,
        obterEvento, atualizarEvento, aguardarEventosProntos, sincronizarEventos,
        adicionarConvidado, removerConvidado, definirStatusConvidado,
        adicionarItemCatalogo, removerItemCatalogo,
        alternarTarefa, adicionarTarefa, removerTarefa, tarefasPadrao,
        obterFavoritos, ehFavorito, alternarFavorito,
        obterNotificacoes, marcarNotificacoesLidas, marcarNotificacaoRespondida, sincronizarNotificacoes,
        obterColaboradores, adicionarColaborador, reenviarConviteColaborador,
        obterConvitePorToken, responderColaborador, definirPermissaoColaborador, removerColaborador,
        obterItensCompartilhados, adicionarItemCompartilhado, assumirItemCompartilhado,
        liberarItemCompartilhado, removerItemCompartilhado,
        obterRateio, definirRateio, calcularRateio,
        adicionarDespesa, removerDespesa, enviarComprovanteDespesa, obterResumoEvento, enviarFoto, removerFoto
    };
})();
