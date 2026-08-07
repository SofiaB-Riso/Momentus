const Momentus = (() => {

    const CHAVE_TEMA = 'momentus:tema';
    const CHAVE_IDIOMA = 'momentus:idioma';
    const CHAVE_PERFIL = 'momentus:perfil';
    const CHAVE_PREFS = 'momentus:preferencias';
    const CHAVE_FAVORITOS = 'momentus:favoritos';
    const CHAVE_NOTIFICACOES = 'momentus:notificacoes';

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
            catBuscaPlaceholder: 'Buscar no catálogo...',
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
            confPagamento: 'Método de pagamento', confPagamentoDesc: 'Cartão terminado em 4471', confAlterar: 'Alterar',
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
            catBuscaPlaceholder: 'Search the catalog...',
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
            confPagamento: 'Payment method', confPagamentoDesc: 'Card ending in 4471', confAlterar: 'Change',
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
            catBuscaPlaceholder: 'Buscar en el catálogo...',
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
            confPagamento: 'Método de pago', confPagamentoDesc: 'Tarjeta terminada en 4471', confAlterar: 'Cambiar',
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

    /* ================= PERFIL ================= */

    function obterPerfil() {
        try {
            const dado = JSON.parse(localStorage.getItem(CHAVE_PERFIL));
            if (dado && dado.nome) return dado;
        } catch (e) { /* ignora */ }
        return { nome: 'Juliana Martins', email: 'juliana.martins@email.com', telefone: '(31) 99999-0000' };
    }

    function salvarPerfil(perfil) {
        localStorage.setItem(CHAVE_PERFIL, JSON.stringify(perfil));
        document.dispatchEvent(new CustomEvent('momentus:perfil-alterado'));
    }

    function iniciais(nome) {
        return nome.split(' ').filter(Boolean).slice(0, 2).map((p) => p[0].toUpperCase()).join('') || 'JM';
    }

    function aplicarPerfilNaTela() {
        const perfil = obterPerfil();
        document.querySelectorAll('.perfilNome').forEach((el) => { el.textContent = perfil.nome; });
        document.querySelectorAll('.avatarPerfil, .avatarTopo').forEach((el) => { el.textContent = iniciais(perfil.nome); });
        document.querySelectorAll('.avatarGrande').forEach((el) => {
            el.childNodes[0] && el.childNodes[0].nodeType === 3
                ? (el.childNodes[0].textContent = iniciais(perfil.nome) + ' ')
                : null;
        });
        const primeiroNome = perfil.nome.split(' ')[0] || perfil.nome;
        document.querySelectorAll('[data-nome-usuario]').forEach((el) => { el.textContent = primeiroNome; });
    }

    /* ================= PREFERÊNCIAS (toggles) ================= */

    function obterPreferencias() {
        try {
            const p = JSON.parse(localStorage.getItem(CHAVE_PREFS));
            if (p) return p;
        } catch (e) { /* ignora */ }
        return { rsvp: true, lembretes: true, novidades: false };
    }

    function salvarPreferencias(prefs) {
        localStorage.setItem(CHAVE_PREFS, JSON.stringify(prefs));
    }

    /* ================= EVENTOS =================
       Antes: tudo lido/gravado direto no localStorage.
       Agora: os eventos vivem no backend (Flask + banco de dados) e o
       front mantém um cache em memória sincronizado com a API. As
       funções abaixo (obterEventos, obterEvento, salvarEvento,
       removerEvento, atualizarEvento) têm a MESMA assinatura de antes,
       então o resto do app (eventos.js, evento.js, script.js) não
       precisou mudar a forma como chama o Momentus.

       Como o backend original só guarda 5 campos (nome, tipo, data,
       endereço e orçamento), tudo o que é específico do front — hora,
       convidados, tarefas, colaboradores, itens do catálogo, rateio,
       lista compartilhada etc. — vai dentro de uma coluna nova,
       "dados_evento" (um JSON). Veja o aviso enviado junto com esta
       entrega para o que mudou no backend. */

    function tarefasPadrao() {
        return [
            { id: 't1', chave: 'checklistLocal', feita: false },
            { id: 't2', chave: 'checklistCardapio', feita: false },
            { id: 't3', chave: 'checklistConvites', feita: false },
            { id: 't4', chave: 'checklistFornecedores', feita: false }
        ];
    }

    // Converte o evento do "formato do front" para o payload que a API espera.
    function eventoParaPayloadAPI(evento) {
        const extras = Object.assign({}, evento);
        delete extras.id;
        delete extras.nome;
        delete extras.tipo;
        delete extras.data;
        delete extras.local;
        delete extras.orcamento;

        return {
            nome_evento: (evento.nome || evento.tipoLabel || 'Evento').toString(),
            tipo_evento: (evento.tipo || 'evento').toString(),
            data_evento: evento.data,
            endereco_evento: evento.local || '',
            orcamento_evento: Number(evento.orcamento) || 0,
            dados_evento: JSON.stringify(extras)
        };
    }

    // Converte o registro que vem da API de volta para o "formato do front".
    function eventoDaAPI(registro) {
        let extras = {};
        if (registro.dados_evento) {
            try { extras = JSON.parse(registro.dados_evento) || {}; } catch (e) { extras = {}; }
        }
        return Object.assign({
            tipoLabel: registro.tipo_evento,
            hora: '—',
            convidados: 0,
            estilo: '',
            observacoes: '',
            status: 'agendado',
            progresso: 0,
            criadoEm: new Date().toISOString(),
            listaConvidados: [],
            itensCatalogo: [],
            tarefas: [],
            colaboradores: [],
            itensCompartilhados: [],
            rateio: { ativo: false, modo: 'auto', valorFixo: 0 }
        }, extras, {
            id: String(registro.id),
            tipo: registro.tipo_evento,
            nome: registro.nome_evento,
            data: registro.data_evento,
            local: registro.endereco_evento,
            orcamento: registro.orcamento_evento
        });
    }

    let _eventosCache = [];
    let _resolverEventosProntos;
    const _eventosProntos = new Promise((resolve) => { _resolverEventosProntos = resolve; });

    function avisarErro(erro, mensagemPadrao) {
        console.error('Momentus:', erro);
        const texto = (erro && erro.message) || mensagemPadrao;
        if (typeof window.mostrarToast === 'function') window.mostrarToast(texto);
    }

    // Busca os eventos no backend e preenche o cache em memória.
    // Todas as páginas escutam "momentus:eventos-alterados" e se
    // redesenham sozinhas quando isso dispara.
    async function sincronizarEventos() {
        try {
            const registros = await MomentusAPI.listarEventos();
            _eventosCache = (registros || []).map(eventoDaAPI);
        } catch (erro) {
            avisarErro(erro, 'Não foi possível carregar os eventos do servidor.');
        } finally {
            document.dispatchEvent(new CustomEvent('momentus:eventos-alterados'));
            _resolverEventosProntos();
        }
    }

    // Promise que resolve quando a primeira sincronização com o backend
    // termina. As páginas usam isso para esperar os dados reais antes
    // de fazer a primeira renderização (evita mostrar "vazio" por um
    // instante enquanto a API ainda está respondendo).
    function aguardarEventosProntos() {
        return _eventosProntos;
    }

    function obterEventos() {
        return _eventosCache.slice();
    }

    function obterEvento(id) {
        const alvo = String(id);
        return _eventosCache.find((ev) => String(ev.id) === alvo) || null;
    }

    async function salvarEvento(evento) {
        evento.criadoEm = evento.criadoEm || new Date().toISOString();
        try {
            const criado = await MomentusAPI.criarEvento(eventoParaPayloadAPI(evento));
            const novoEvento = eventoDaAPI(criado);
            _eventosCache.push(novoEvento);
            document.dispatchEvent(new CustomEvent('momentus:eventos-alterados'));
            return novoEvento;
        } catch (erro) {
            avisarErro(erro, 'Não foi possível salvar o evento.');
            return null;
        }
    }

    async function removerEvento(id) {
        try {
            await MomentusAPI.removerEvento(id);
            _eventosCache = _eventosCache.filter((ev) => String(ev.id) !== String(id));
            document.dispatchEvent(new CustomEvent('momentus:eventos-alterados'));
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

    // Ponto único por onde passam TODAS as alterações de evento
    // (convidados, tarefas, colaboradores, itens, rateio...). Mescla os
    // dados novos com o evento atual e manda o objeto completo pro
    // backend (PUT), igual o back já esperava.
    async function atualizarEvento(id, dadosNovos) {
        const atual = obterEvento(id);
        if (!atual) return null;
        const mesclado = Object.assign({}, atual, dadosNovos);

        try {
            const registro = await MomentusAPI.atualizarEvento(id, eventoParaPayloadAPI(mesclado));
            const eventoAtualizado = eventoDaAPI(registro);
            const idx = _eventosCache.findIndex((ev) => String(ev.id) === String(id));
            if (idx !== -1) _eventosCache[idx] = eventoAtualizado;
            document.dispatchEvent(new CustomEvent('momentus:eventos-alterados'));
            return eventoAtualizado;
        } catch (erro) {
            avisarErro(erro, 'Não foi possível salvar as alterações.');
            return null;
        }
    }

    sincronizarEventos();

    /* ---- Convidados ---- */

    function adicionarConvidado(eventoId, convidado) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const lista = Array.isArray(evento.listaConvidados) ? evento.listaConvidados.slice() : [];
        lista.push({
            id: 'conv-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
            nome: convidado.nome || '',
            contato: convidado.contato || '',
            status: convidado.status || 'pendente'
        });
        const totalConfirmados = lista.filter((c) => c.status === 'confirmado').length;
        return atualizarEvento(eventoId, {
            listaConvidados: lista,
            convidados: Math.max(evento.convidados || 0, totalConfirmados, lista.length)
        });
    }

    function removerConvidado(eventoId, convidadoId) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const lista = (evento.listaConvidados || []).filter((c) => c.id !== convidadoId);
        return atualizarEvento(eventoId, { listaConvidados: lista });
    }

    function definirStatusConvidado(eventoId, convidadoId, status) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const lista = (evento.listaConvidados || []).map((c) => c.id === convidadoId ? Object.assign({}, c, { status }) : c);
        return atualizarEvento(eventoId, { listaConvidados: lista });
    }

    /* ---- Itens do catálogo por evento ---- */

    function adicionarItemCatalogo(eventoId, item) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const lista = Array.isArray(evento.itensCatalogo) ? evento.itensCatalogo.slice() : [];
        const existente = lista.find((i) => i.produtoId === item.produtoId);
        if (existente) {
            existente.qtd = (existente.qtd || 1) + 1;
        } else {
            lista.push(Object.assign({ id: 'item-' + Date.now() + '-' + Math.floor(Math.random() * 1000), qtd: 1 }, item));
        }
        return atualizarEvento(eventoId, { itensCatalogo: lista });
    }

    function removerItemCatalogo(eventoId, itemId) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const lista = (evento.itensCatalogo || []).filter((i) => i.id !== itemId);
        return atualizarEvento(eventoId, { itensCatalogo: lista });
    }

    /* ---- Notificações (caixa de notificação) ---- */

    function obterNotificacoes() {
        try {
            const n = JSON.parse(localStorage.getItem(CHAVE_NOTIFICACOES));
            if (Array.isArray(n)) return n;
        } catch (e) { /* ignora */ }
        return [];
    }

    function salvarNotificacoes(lista) {
        localStorage.setItem(CHAVE_NOTIFICACOES, JSON.stringify(lista));
        document.dispatchEvent(new CustomEvent('momentus:notificacoes-alteradas'));
    }

    function criarNotificacao(dados) {
        const lista = obterNotificacoes();
        lista.unshift(Object.assign({
            id: 'notif-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
            lida: false,
            respondida: false,
            criadoEm: Date.now()
        }, dados));
        salvarNotificacoes(lista);
        return lista[0];
    }

    function marcarNotificacoesLidas() {
        const lista = obterNotificacoes().map((n) => Object.assign({}, n, { lida: true }));
        salvarNotificacoes(lista);
    }

    function marcarNotificacaoRespondida(notifId, resposta) {
        const lista = obterNotificacoes().map((n) => n.id === notifId ? Object.assign({}, n, { lida: true, respondida: true, resposta }) : n);
        salvarNotificacoes(lista);
    }

    function removerNotificacaoDoConvite(colaboradorId) {
        const lista = obterNotificacoes().filter((n) => n.colaboradorId !== colaboradorId);
        salvarNotificacoes(lista);
    }

    /* ---- Colaboradores (junta-panelas: gestão de acesso) ---- */

    function gerarToken() {
        return 'tok-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);
    }

    function obterColaboradores(eventoId) {
        const evento = obterEvento(eventoId);
        return evento ? (evento.colaboradores || []) : [];
    }

    function adicionarColaborador(eventoId, dados) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const lista = Array.isArray(evento.colaboradores) ? evento.colaboradores.slice() : [];
        const colaborador = {
            id: 'colab-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
            nome: (dados.nome || '').trim(),
            contato: (dados.contato || '').trim(),
            status: 'pendente',
            token: gerarToken(),
            criadoEm: Date.now()
        };
        lista.push(colaborador);
        atualizarEvento(eventoId, { colaboradores: lista });

        // Simula o convite chegando na caixa de notificação da pessoa convidada
        criarNotificacao({
            tipo: 'convite-colaborador',
            eventoId: eventoId,
            colaboradorId: colaborador.id,
            token: colaborador.token,
            eventoNome: evento.nome || evento.tipoLabel,
            convidadoNome: colaborador.nome,
            convidadoContato: colaborador.contato
        });

        return colaborador;
    }

    function reenviarConviteColaborador(eventoId, colaboradorId) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const colaborador = (evento.colaboradores || []).find((c) => c.id === colaboradorId);
        if (!colaborador) return null;
        removerNotificacaoDoConvite(colaboradorId);
        criarNotificacao({
            tipo: 'convite-colaborador',
            eventoId: eventoId,
            colaboradorId: colaborador.id,
            token: colaborador.token,
            eventoNome: evento.nome || evento.tipoLabel,
            convidadoNome: colaborador.nome,
            convidadoContato: colaborador.contato
        });
        return colaborador;
    }

    function obterConvitePorToken(token) {
        const eventos = obterEventos();
        for (let i = 0; i < eventos.length; i++) {
            const colaboradores = eventos[i].colaboradores || [];
            const colaborador = colaboradores.find((c) => c.token === token);
            if (colaborador) return { evento: eventos[i], colaborador };
        }
        return null;
    }

    function responderColaborador(eventoId, colaboradorId, status) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const lista = (evento.colaboradores || []).map((c) => c.id === colaboradorId ? Object.assign({}, c, { status }) : c);
        const atualizado = atualizarEvento(eventoId, { colaboradores: lista });
        marcarNotificacaoRespondida(colaboradorId, status);
        return atualizado;
    }

    function removerColaborador(eventoId, colaboradorId) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const lista = (evento.colaboradores || []).filter((c) => c.id !== colaboradorId);
        removerNotificacaoDoConvite(colaboradorId);
        return atualizarEvento(eventoId, { colaboradores: lista });
    }

    /* ---- Rateio de despesas ---- */

    function obterRateio(eventoId) {
        const evento = obterEvento(eventoId);
        const padrao = { ativo: false, modo: 'auto', valorFixo: 0 };
        if (!evento) return padrao;
        return Object.assign({}, padrao, evento.rateio || {});
    }

    function definirRateio(eventoId, dados) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const atual = obterRateio(eventoId);
        const novo = Object.assign({}, atual, dados);
        return atualizarEvento(eventoId, { rateio: novo });
    }

    function calcularRateio(eventoId) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const rateio = obterRateio(eventoId);

        const totalDespesas = (evento.itensCatalogo || []).reduce((soma, item) => {
            return soma + (Number(item.preco) || 0) * (item.qtd || 1);
        }, 0);

        const colaboradoresAtivos = (evento.colaboradores || []).filter((c) => c.status === 'ativo');
        const qtdPessoas = 1 + colaboradoresAtivos.length; // organizador + colaboradores ativos

        let valorPorPessoa = 0;
        if (rateio.modo === 'fixo') {
            valorPorPessoa = Number(rateio.valorFixo) || 0;
        } else {
            valorPorPessoa = qtdPessoas > 0 ? totalDespesas / qtdPessoas : 0;
        }

        const pessoas = [{ id: 'organizador', nome: t('rateioVoce'), valor: valorPorPessoa, organizador: true }]
            .concat(colaboradoresAtivos.map((c) => ({ id: c.id, nome: c.nome || '—', valor: valorPorPessoa, organizador: false })));

        return {
            ativo: !!rateio.ativo,
            modo: rateio.modo,
            valorFixo: Number(rateio.valorFixo) || 0,
            totalDespesas,
            qtdPessoas,
            valorPorPessoa,
            totalArrecadado: valorPorPessoa * qtdPessoas,
            pessoas
        };
    }

    /* ---- Lista compartilhada de itens (junta-panelas) ---- */

    function obterItensCompartilhados(eventoId) {
        const evento = obterEvento(eventoId);
        return evento ? (evento.itensCompartilhados || []) : [];
    }

    function encontrarItemCompartilhadoPorNome(eventoId, nome) {
        const alvo = (nome || '').trim().toLowerCase();
        return obterItensCompartilhados(eventoId).find((it) => (it.nome || '').trim().toLowerCase() === alvo) || null;
    }

    function adicionarItemCompartilhado(eventoId, dados) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const existente = encontrarItemCompartilhadoPorNome(eventoId, dados.nome);
        if (existente) return { duplicado: true, item: existente };

        const lista = Array.isArray(evento.itensCompartilhados) ? evento.itensCompartilhados.slice() : [];
        const item = {
            id: 'compart-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
            nome: (dados.nome || '').trim(),
            quantidade: Math.max(1, Number(dados.quantidade) || 1),
            responsavelId: null,
            responsavelNome: '',
            criadoEm: Date.now()
        };
        lista.push(item);
        atualizarEvento(eventoId, { itensCompartilhados: lista });
        return { duplicado: false, item };
    }

    function assumirItemCompartilhado(eventoId, itemId, responsavel) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const lista = (evento.itensCompartilhados || []).map((it) => it.id === itemId
            ? Object.assign({}, it, { responsavelId: responsavel.responsavelId || null, responsavelNome: responsavel.responsavelNome || '' })
            : it);
        return atualizarEvento(eventoId, { itensCompartilhados: lista });
    }

    function liberarItemCompartilhado(eventoId, itemId) {
        return assumirItemCompartilhado(eventoId, itemId, { responsavelId: null, responsavelNome: '' });
    }

    function removerItemCompartilhado(eventoId, itemId) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const lista = (evento.itensCompartilhados || []).filter((it) => it.id !== itemId);
        return atualizarEvento(eventoId, { itensCompartilhados: lista });
    }

    /* ---- Tarefas / checklist ---- */

    function alternarTarefa(eventoId, tarefaId) {
        const evento = obterEvento(eventoId);
        if (!evento) return null;
        const tarefas = (Array.isArray(evento.tarefas) && evento.tarefas.length ? evento.tarefas : tarefasPadrao())
            .map((tf) => tf.id === tarefaId ? Object.assign({}, tf, { feita: !tf.feita }) : tf);
        const feitas = tarefas.filter((tf) => tf.feita).length;
        const progresso = tarefas.length ? Math.round((feitas / tarefas.length) * 100) : 0;
        return atualizarEvento(eventoId, { tarefas, progresso });
    }

    /* ---- Favoritos (catálogo) ---- */

    function obterFavoritos() {
        try {
            const f = JSON.parse(localStorage.getItem(CHAVE_FAVORITOS));
            if (Array.isArray(f)) return f;
        } catch (e) { /* ignora */ }
        return [];
    }

    function ehFavorito(produtoId) {
        return obterFavoritos().indexOf(produtoId) !== -1;
    }

    function alternarFavorito(produtoId) {
        let favoritos = obterFavoritos();
        if (favoritos.indexOf(produtoId) !== -1) {
            favoritos = favoritos.filter((f) => f !== produtoId);
        } else {
            favoritos.push(produtoId);
        }
        localStorage.setItem(CHAVE_FAVORITOS, JSON.stringify(favoritos));
        document.dispatchEvent(new CustomEvent('momentus:favoritos-alterados'));
        return favoritos;
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
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', iniciar);
    } else {
        iniciar();
    }

    return {
        t, obterIdioma, aplicarIdioma, obterMeses, obterMesesAbrev, obterSemanaCurta,
        obterTema, aplicarTema, alternarTema,
        obterPerfil, salvarPerfil, iniciais, aplicarPerfilNaTela,
        obterPreferencias, salvarPreferencias,
        obterEventos, salvarEvento, removerEvento, diasEntre,
        obterEvento, atualizarEvento, aguardarEventosProntos,
        adicionarConvidado, removerConvidado, definirStatusConvidado,
        adicionarItemCatalogo, removerItemCatalogo,
        alternarTarefa, tarefasPadrao,
        obterFavoritos, ehFavorito, alternarFavorito,
        obterNotificacoes, marcarNotificacoesLidas, marcarNotificacaoRespondida,
        obterColaboradores, adicionarColaborador, reenviarConviteColaborador,
        obterConvitePorToken, responderColaborador, removerColaborador,
        obterItensCompartilhados, adicionarItemCompartilhado, assumirItemCompartilhado,
        liberarItemCompartilhado, removerItemCompartilhado,
        obterRateio, definirRateio, calcularRateio
    };
})();
