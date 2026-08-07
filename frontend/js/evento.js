/* ================= PÁGINA DO EVENTO (individual) ================= */
(function () {
    const container = document.getElementById('conteudoEvento');
    if (!container) return;

    const params = new URLSearchParams(window.location.search);
    const eventoId = params.get('id');

    const botaoVoltar = document.getElementById('botaoVoltar');
    if (botaoVoltar) {
        botaoVoltar.addEventListener('click', () => {
            if (document.referrer && document.referrer.indexOf(window.location.origin) === 0) {
                window.history.back();
            } else {
                window.location.href = 'eventos.html';
            }
        });
    }

    const CATEGORIA_COR = {
        salgados: 'var(--grad-2)', doces: 'var(--grad-1)', bebidas: 'linear-gradient(135deg,#6a8dff,#8a5cf6)',
        decoracao: 'linear-gradient(135deg,#f0a63a,#f7cf6e)', buffet: 'var(--grad-3)'
    };

    function montarVazio() {
        const tpl = document.getElementById('templateEventoVazio');
        container.innerHTML = '';
        container.appendChild(tpl.content.cloneNode(true));
        // "false" = só traduz o HTML que acabou de ser inserido; não é uma
        // troca de idioma de verdade, então não deve disparar
        // "momentus:idioma-alterado" (isso causava um loop infinito, já
        // que esta própria página escuta esse evento para se redesenhar).
        Momentus.aplicarIdioma(Momentus.obterIdioma(), false);
    }

    function abaAtivaAtual() {
        const ativa = container.querySelector('.abaEvento.abaAtiva');
        return ativa ? ativa.dataset.aba : 'informacoes';
    }

    function renderizarEvento() {
        const evento = Momentus.obterEvento(eventoId);
        if (!evento) { montarVazio(); return; }

        const abaAntes = container.querySelector('.abaEvento') ? abaAtivaAtual() : 'informacoes';

        const tpl = document.getElementById('templateEvento');
        container.innerHTML = '';
        container.appendChild(tpl.content.cloneNode(true));

        document.title = (evento.nome || evento.tipoLabel) + ' - Momentus';

        container.querySelector('#tagTipoEvento').textContent = evento.tipoLabel || '';
        container.querySelector('#tituloEvento').textContent = evento.nome || evento.tipoLabel;
        container.querySelector('#localEventoTexto').textContent = evento.local || '—';
        container.querySelector('#dataHoraEventoTexto').textContent = `${formatarDataBR(evento.data)}${evento.hora && evento.hora !== '—' ? ' · ' + evento.hora : ''}`;

        const statusChave = STATUS_LABEL_CHAVE[evento.status] || 'statusAgendado';
        container.querySelector('#statusPillEvento').textContent = Momentus.t(statusChave);

        const progresso = evento.progresso || 0;
        container.querySelector('#progressoTexto').textContent = progresso + '%';
        container.querySelector('#progressoBarra').style.width = progresso + '%';

        // Informações
        container.querySelector('#infoLocal').textContent = evento.local || '—';
        container.querySelector('#infoDataHora').textContent = `${formatarDataBR(evento.data)}${evento.hora && evento.hora !== '—' ? ' · ' + evento.hora : ''}`;
        container.querySelector('#infoConvidados').textContent = evento.convidados ? `${evento.convidados} ${Momentus.t('resumoConvidadosSufixo')}` : '—';
        container.querySelector('#infoEstilo').textContent = evento.estilo || '—';
        container.querySelector('#infoOrcamento').textContent = formatarMoeda(evento.orcamento || 0);
        const gasto = (evento.itensCatalogo || []).reduce((soma, it) => soma + (Number(it.preco) || 0) * (it.qtd || 1), 0);
        container.querySelector('#infoGasto').textContent = formatarMoeda(gasto);
        container.querySelector('#infoObservacoes').textContent = evento.observacoes && evento.observacoes.trim() ? evento.observacoes : Momentus.t('semObservacoes');

        // Abas
        const abas = container.querySelectorAll('.abaEvento');
        const paineis = container.querySelectorAll('.painelAba');
        function ativarAba(nome) {
            abas.forEach((a) => a.classList.toggle('abaAtiva', a.dataset.aba === nome));
            paineis.forEach((p) => p.classList.toggle('ativoPainel', p.dataset.painel === nome));
        }
        abas.forEach((a) => a.addEventListener('click', () => ativarAba(a.dataset.aba)));
        ativarAba(abaAntes);

        // Ações do cabeçalho
        container.querySelector('#botaoEditarEvento').addEventListener('click', () => {
            window.location.href = 'planejar.html?id=' + encodeURIComponent(evento.id);
        });
        container.querySelector('#botaoApagarEvento').addEventListener('click', async () => {
            if (window.confirm(Momentus.t('confirmarApagarEvento', { nome: evento.nome || evento.tipoLabel }))) {
                const removeu = await Momentus.removerEvento(evento.id);
                if (removeu) window.location.href = 'eventos.html';
            }
        });

        renderizarConvidados(evento);
        renderizarColaboradores(evento);
        renderizarItensCompartilhados(evento);
        renderizarItens(evento);
        renderizarTarefas(evento);
        ligarRateio(evento);

        // Botão de adicionar colaborador (dentro do template, precisa ser religado a cada render)
        const botaoAddColab = container.querySelector('#botaoAdicionarColaborador');
        if (botaoAddColab) botaoAddColab.addEventListener('click', () => abrirModalColaborador());
        ligarFormularioItemCompartilhado(evento);

        // Formulário de convidado
        const formConvidado = container.querySelector('#formConvidado');
        formConvidado.addEventListener('submit', (e) => {
            e.preventDefault();
            const nome = container.querySelector('#nomeNovoConvidado').value.trim();
            const contato = container.querySelector('#contatoNovoConvidado').value.trim();
            if (!nome) return;
            Momentus.adicionarConvidado(evento.id, { nome, contato });
        });

        // Mesmo motivo do comentário em montarVazio(): só re-traduz o DOM,
        // não notifica (evita o loop infinito de re-render).
        Momentus.aplicarIdioma(Momentus.obterIdioma(), false);
    }

    function renderizarConvidados(evento) {
        const lista = evento.listaConvidados || [];
        const listaEl = container.querySelector('#listaConvidados');
        const resumoEl = container.querySelector('#resumoConvidadosLinha');

        const confirmados = lista.filter((c) => c.status === 'confirmado').length;
        const pendentes = lista.filter((c) => c.status === 'pendente').length;
        const recusados = lista.filter((c) => c.status === 'recusado').length;
        resumoEl.innerHTML = lista.length
            ? `<span><strong>${confirmados}</strong> ${Momentus.t('statusConvidadoConfirmado').toLowerCase()}</span><span><strong>${pendentes}</strong> ${Momentus.t('statusConvidadoPendente').toLowerCase()}</span><span><strong>${recusados}</strong> ${Momentus.t('statusConvidadoRecusado').toLowerCase()}</span>`
            : '';

        if (!lista.length) {
            listaEl.innerHTML = `<p class="estadoVazioClaro" style="text-align:left; padding-left:0;">${Momentus.t('nenhumConvidado')}</p>`;
            return;
        }

        const tplLinha = document.getElementById('templateLinhaConvidado');
        listaEl.innerHTML = '';
        lista.forEach((conv) => {
            const linha = tplLinha.content.cloneNode(true);
            const raiz = linha.querySelector('.linhaConvidado');
            raiz.dataset.id = conv.id;
            raiz.querySelector('.avatarConvidado').textContent = Momentus.iniciais(conv.nome || '?');
            raiz.querySelector('.nomeConvidado').textContent = conv.nome || '—';
            raiz.querySelector('.contatoConvidado').textContent = conv.contato || '—';
            const select = raiz.querySelector('.selectStatusConvidado');
            select.value = conv.status || 'pendente';
            select.querySelectorAll('option').forEach((op) => { op.textContent = Momentus.t(op.getAttribute('data-i18n')); });
            select.addEventListener('change', () => {
                Momentus.definirStatusConvidado(evento.id, conv.id, select.value);
            });
            raiz.querySelector('.botaoRemoverConvidado').addEventListener('click', () => {
                Momentus.removerConvidado(evento.id, conv.id);
            });
            listaEl.appendChild(linha);
        });
    }

    function renderizarItens(evento) {
        const lista = evento.itensCatalogo || [];
        const listaEl = container.querySelector('#listaItensEvento');
        const rodape = container.querySelector('#rodapeTotalItens');

        if (!lista.length) {
            listaEl.innerHTML = `<p class="estadoVazioClaro" style="text-align:left; padding-left:0;">${Momentus.t('nenhumItemCatalogo')}</p>`;
            rodape.style.display = 'none';
            return;
        }

        const tplLinha = document.getElementById('templateLinhaItem');
        listaEl.innerHTML = '';
        let total = 0;
        lista.forEach((item) => {
            const subtotal = (Number(item.preco) || 0) * (item.qtd || 1);
            total += subtotal;
            const linha = tplLinha.content.cloneNode(true);
            const raiz = linha.querySelector('.linhaItemEvento');
            raiz.dataset.id = item.id;
            const thumb = raiz.querySelector('.thumbItemEvento');
            thumb.style.background = CATEGORIA_COR[item.categoria] || 'var(--grad-1)';
            raiz.querySelector('.nomeItemEvento').textContent = item.nome || '—';
            raiz.querySelector('.metaItemEvento').textContent = (item.qtd || 1) > 1 ? `${item.qtd}x` : '';
            raiz.querySelector('.precoItemEvento').textContent = formatarMoeda(subtotal);
            raiz.querySelector('.botaoRemoverConvidado').addEventListener('click', () => {
                Momentus.removerItemCatalogo(evento.id, item.id);
            });
            listaEl.appendChild(linha);
        });
        rodape.style.display = 'flex';
        container.querySelector('#totalItensValor').textContent = formatarMoeda(total);
    }

    const STATUS_COLAB_CHAVE = {
        pendente: 'statusColabPendente',
        ativo: 'statusColabAtivo',
        recusado: 'statusColabRecusado'
    };

    function renderizarColaboradores(evento) {
        const lista = evento.colaboradores || [];
        const listaEl = container.querySelector('#listaColaboradores');
        if (!listaEl) return;

        if (!lista.length) {
            listaEl.innerHTML = `<p class="estadoVazioClaro" style="text-align:left; padding-left:0;">${Momentus.t('nenhumColaborador')}</p>`;
            return;
        }

        const tplLinha = document.getElementById('templateLinhaColaborador');
        listaEl.innerHTML = '';
        lista.forEach((colab) => {
            const linha = tplLinha.content.cloneNode(true);
            const raiz = linha.querySelector('.linhaColaborador');
            raiz.dataset.id = colab.id;
            raiz.querySelector('.avatarConvidado').textContent = Momentus.iniciais(colab.nome || '?');
            raiz.querySelector('.nomeConvidado').textContent = colab.nome || '—';
            raiz.querySelector('.contatoConvidado').textContent = colab.contato || '—';

            const pill = raiz.querySelector('.statusPillColab');
            pill.textContent = Momentus.t(STATUS_COLAB_CHAVE[colab.status] || 'statusColabPendente');
            pill.classList.add(colab.status || 'pendente');

            const botaoReenviar = raiz.querySelector('.botaoTextoReenviar');
            if (colab.status === 'pendente') {
                botaoReenviar.style.display = '';
                botaoReenviar.addEventListener('click', () => {
                    Momentus.reenviarConviteColaborador(evento.id, colab.id);
                    mostrarToast(Momentus.t('conviteReenviado'));
                });
            }

            raiz.querySelector('.botaoRemoverConvidado').addEventListener('click', () => {
                if (window.confirm(Momentus.t('confirmarRemoverColaborador', { nome: colab.nome || '' }))) {
                    Momentus.removerColaborador(evento.id, colab.id);
                }
            });
            listaEl.appendChild(linha);
        });
    }

    /* ---- Módulo: rateio de despesas ---- */

    function renderizarRateio(evento) {
        const dados = Momentus.calcularRateio(evento.id);
        if (!dados) return;

        const opcoes = container.querySelector('#opcoesRateio');
        opcoes.style.display = dados.ativo ? '' : 'none';
        if (!dados.ativo) return;

        container.querySelector('#rateioTotalDespesasValor').textContent = formatarMoeda(dados.totalDespesas);
        container.querySelector('#rateioQtdPessoasValor').textContent = dados.qtdPessoas;
        container.querySelector('#rateioValorPorPessoaValor').textContent = formatarMoeda(dados.valorPorPessoa);

        const listaEl = container.querySelector('#listaRateioPessoas');
        listaEl.innerHTML = '';

        if (dados.modo === 'auto' && !dados.totalDespesas) {
            listaEl.innerHTML = `<p class="estadoVazioClaro" style="text-align:left; padding-left:0;">${Momentus.t('rateioAvisoSemDespesas')}</p>`;
        } else {
            dados.pessoas.forEach((pessoa) => {
                const linha = document.createElement('div');
                linha.className = 'itemRateioPessoa';
                linha.innerHTML = `
                    <span class="nomeRateioPessoa">${pessoa.nome}${pessoa.organizador ? `<span class="tagOrganizador">${Momentus.t('rateioVoce')}</span>` : ''}</span>
                    <span class="valorRateioPessoa">${formatarMoeda(pessoa.valor)}</span>`;
                listaEl.appendChild(linha);
            });
            if (dados.pessoas.length === 1) {
                const aviso = document.createElement('p');
                aviso.className = 'estadoVazioClaro';
                aviso.style.textAlign = 'left';
                aviso.style.paddingLeft = '0';
                aviso.textContent = Momentus.t('rateioSemColaboradoresAtivos');
                listaEl.appendChild(aviso);
            }
        }
    }

    function ligarRateio(evento) {
        const checkboxAtivar = container.querySelector('#checkboxAtivarRateio');
        const radioAuto = container.querySelector('#radioRateioAuto');
        const radioFixo = container.querySelector('#radioRateioFixo');
        const campoValorFixo = container.querySelector('#campoValorFixoRateio');
        const inputValorFixo = container.querySelector('#valorFixoRateio');
        if (!checkboxAtivar) return;

        const rateio = Momentus.obterRateio(evento.id);
        checkboxAtivar.checked = !!rateio.ativo;
        radioAuto.checked = rateio.modo !== 'fixo';
        radioFixo.checked = rateio.modo === 'fixo';
        campoValorFixo.style.display = rateio.modo === 'fixo' ? '' : 'none';
        if (rateio.valorFixo) inputValorFixo.value = rateio.valorFixo;

        renderizarRateio(evento);

        checkboxAtivar.addEventListener('change', () => {
            Momentus.definirRateio(evento.id, { ativo: checkboxAtivar.checked });
        });

        [radioAuto, radioFixo].forEach((radio) => {
            radio.addEventListener('change', () => {
                const modo = radioFixo.checked ? 'fixo' : 'auto';
                campoValorFixo.style.display = modo === 'fixo' ? '' : 'none';
                Momentus.definirRateio(evento.id, { modo });
            });
        });

        inputValorFixo.addEventListener('change', () => {
            Momentus.definirRateio(evento.id, { modo: 'fixo', valorFixo: Number(inputValorFixo.value) || 0 });
        });
    }

    function renderizarItensCompartilhados(evento) {
        const lista = evento.itensCompartilhados || [];
        const listaEl = container.querySelector('#listaItensCompartilhados');
        if (!listaEl) return;

        if (!lista.length) {
            listaEl.innerHTML = `<p class="estadoVazioClaro" style="text-align:left; padding-left:0;">${Momentus.t('nenhumItemCompartilhado')}</p>`;
            return;
        }

        const tplLinha = document.getElementById('templateLinhaItemCompartilhado');
        listaEl.innerHTML = '';
        lista.forEach((item) => {
            const linha = tplLinha.content.cloneNode(true);
            const raiz = linha.querySelector('.linhaItemCompartilhado');
            raiz.dataset.id = item.id;
            const qtdTexto = (item.quantidade || 1) > 1 ? `${item.quantidade}x` : '';
            raiz.querySelector('.nomeItemEvento').textContent = qtdTexto ? `${item.nome} · ${qtdTexto}` : item.nome;

            const metaEl = raiz.querySelector('.metaResponsavelItem');
            const botaoAssumir = raiz.querySelector('.botaoAssumirItem');

            if (item.responsavelNome) {
                metaEl.textContent = Momentus.t('levadoPor', { nome: item.responsavelNome });
                metaEl.classList.add('temResponsavel');
                botaoAssumir.textContent = Momentus.t('botaoLiberarItem');
                botaoAssumir.addEventListener('click', () => {
                    Momentus.liberarItemCompartilhado(evento.id, item.id);
                });
            } else {
                metaEl.textContent = Momentus.t('itemSemResponsavel');
                botaoAssumir.textContent = Momentus.t('botaoEuVouLevar');
                botaoAssumir.addEventListener('click', () => abrirModalEscolherResponsavel(evento, item));
            }

            raiz.querySelector('.botaoRemoverConvidado').addEventListener('click', () => {
                Momentus.removerItemCompartilhado(evento.id, item.id);
            });
            listaEl.appendChild(linha);
        });
    }

    /* ---- Formulário: novo item da lista compartilhada (junta-panelas) ---- */
    function ligarFormularioItemCompartilhado(evento) {
        const form = container.querySelector('#formItemCompartilhado');
        if (!form) return;
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const nomeInput = container.querySelector('#nomeNovoItemCompartilhado');
            const qtdInput = container.querySelector('#qtdNovoItemCompartilhado');
            const nome = nomeInput.value.trim();
            if (!nome) return;
            const resultado = Momentus.adicionarItemCompartilhado(evento.id, { nome, quantidade: qtdInput.value });
            if (resultado && resultado.duplicado) {
                mostrarToast(Momentus.t('itemJaExisteAviso', { nome: resultado.item.nome }));
            }
            nomeInput.value = '';
            qtdInput.value = '1';
        });
    }

    /* ---- Modal: escolher responsável por um item da lista compartilhada ---- */
    const overlayEscolherResponsavel = document.getElementById('overlayEscolherResponsavel');
    const corpoEscolherResponsavel = document.getElementById('corpoEscolherResponsavel');
    const tituloEscolherResponsavel = document.getElementById('tituloEscolherResponsavel');
    const fecharEscolherResponsavelBtn = document.getElementById('fecharEscolherResponsavel');

    function fecharModalEscolherResponsavel() {
        if (overlayEscolherResponsavel) overlayEscolherResponsavel.classList.remove('aberto');
    }
    if (fecharEscolherResponsavelBtn) fecharEscolherResponsavelBtn.addEventListener('click', fecharModalEscolherResponsavel);
    if (overlayEscolherResponsavel) {
        overlayEscolherResponsavel.addEventListener('click', (e) => {
            if (e.target === overlayEscolherResponsavel) fecharModalEscolherResponsavel();
        });
    }

    function abrirModalEscolherResponsavel(evento, item) {
        if (!overlayEscolherResponsavel) return;
        tituloEscolherResponsavel.textContent = Momentus.t('escolherResponsavelTitulo', { item: item.nome });
        const colaboradoresAtivos = (evento.colaboradores || []).filter((c) => c.status === 'ativo');

        const perfil = Momentus.obterPerfil();
        const opcoes = [{ id: null, nome: perfil.nome || Momentus.t('opcaoEuMesma') }].concat(
            colaboradoresAtivos.map((c) => ({ id: c.id, nome: c.nome }))
        );

        corpoEscolherResponsavel.innerHTML = `<div class="listaEscolhaResponsavel">${opcoes.map((op) => `
            <button type="button" class="opcaoResponsavel" data-id="${op.id || ''}">
                <span class="avatarConvidado" style="width:2.1rem;height:2.1rem;font-size:.78rem;">${Momentus.iniciais(op.nome || '?')}</span>
                <span>${escapeHTML(op.nome || '—')}</span>
            </button>`).join('')}</div>${!colaboradoresAtivos.length ? `<p style="font-size:.76rem; color:var(--tinta-suave); margin-top:.9rem;">${Momentus.t('semColaboradoresParaAssumir')}</p>` : ''}`;

        corpoEscolherResponsavel.querySelectorAll('.opcaoResponsavel').forEach((botao) => {
            botao.addEventListener('click', () => {
                const escolhido = opcoes.find((op) => (op.id || '') === botao.dataset.id);
                Momentus.assumirItemCompartilhado(evento.id, item.id, {
                    responsavelId: escolhido && escolhido.id,
                    responsavelNome: escolhido ? escolhido.nome : ''
                });
                fecharModalEscolherResponsavel();
            });
        });

        overlayEscolherResponsavel.classList.add('aberto');
    }

    /* ---- Modal: adicionar colaborador (convite por e-mail ou link) ---- */
    const overlayAddColab = document.getElementById('overlayAdicionarColaborador');
    const formAddColab = document.getElementById('formAdicionarColaborador');
    const fecharAddColabBtn = document.getElementById('fecharAdicionarColaborador');

    function fecharModalColaborador() {
        if (overlayAddColab) overlayAddColab.classList.remove('aberto');
        if (formAddColab) formAddColab.reset();
    }
    function abrirModalColaborador() {
        if (!overlayAddColab) return;
        overlayAddColab.classList.add('aberto');
        const campoNome = document.getElementById('nomeNovoColaborador');
        if (campoNome) campoNome.focus();
    }
    if (fecharAddColabBtn) fecharAddColabBtn.addEventListener('click', fecharModalColaborador);
    if (overlayAddColab) {
        overlayAddColab.addEventListener('click', (e) => {
            if (e.target === overlayAddColab) fecharModalColaborador();
        });
    }

    function construirLinkConvite(token) {
        const url = new URL(window.location.href);
        url.search = '';
        url.searchParams.set('id', eventoId);
        url.searchParams.set('convite', token);
        return url.toString();
    }

    async function copiarLink(link) {
        try {
            await navigator.clipboard.writeText(link);
            return true;
        } catch (e) {
            return false;
        }
    }

    if (formAddColab) {
        formAddColab.addEventListener('submit', async (e) => {
            e.preventDefault();
            const evento = Momentus.obterEvento(eventoId);
            if (!evento) return;

            const modo = (e.submitter && e.submitter.dataset && e.submitter.dataset.modo) || 'email';
            const nome = document.getElementById('nomeNovoColaborador').value.trim();
            const email = document.getElementById('emailNovoColaborador').value.trim();

            if (!nome) {
                mostrarToast(Momentus.t('erroPreencherNomeColaborador'));
                return;
            }
            if (modo === 'email' && !email) {
                mostrarToast(Momentus.t('erroPreencherEmailColaborador'));
                return;
            }

            const colaborador = Momentus.adicionarColaborador(evento.id, { nome, contato: email });
            if (!colaborador) return;

            if (modo === 'email') {
                mostrarToast(Momentus.t('conviteEnviadoEmail', { email }));
                fecharModalColaborador();
            } else {
                const link = construirLinkConvite(colaborador.token);
                const copiou = await copiarLink(link);
                if (navigator.share) {
                    try {
                        await navigator.share({ title: 'Momentus', text: Momentus.t('convitePopupTexto', { evento: evento.nome || evento.tipoLabel }), url: link });
                    } catch (err) { /* usuário cancelou o compartilhamento */ }
                }
                mostrarToast(copiou ? Momentus.t('linkCopiado') : Momentus.t('linkNaoCopiado', { link }));
                fecharModalColaborador();
            }
        });
    }

    /* ---- Modal: aceitar/recusar convite recebido por link ---- */
    const overlayConvite = document.getElementById('overlayConviteRecebido');
    const textoConviteRecebido = document.getElementById('textoConviteRecebido');
    const botaoAceitarConvite = document.getElementById('botaoAceitarConvite');
    const botaoRecusarConvite = document.getElementById('botaoRecusarConvite');
    const fecharConviteBtn = document.getElementById('fecharConviteRecebido');

    function fecharModalConvite() {
        if (overlayConvite) overlayConvite.classList.remove('aberto');
        const url = new URL(window.location.href);
        url.searchParams.delete('convite');
        window.history.replaceState({}, '', url.toString());
    }

    function verificarConviteNaUrl() {
        const tokenConvite = params.get('convite');
        if (!tokenConvite || !overlayConvite) return;

        const encontrado = Momentus.obterConvitePorToken(tokenConvite);
        if (!encontrado || encontrado.colaborador.status !== 'pendente') {
            if (encontrado) mostrarToast(Momentus.t('conviteInvalido'));
            fecharModalConvite();
            return;
        }

        const { evento, colaborador } = encontrado;
        textoConviteRecebido.textContent = Momentus.t('convitePopupTexto', { evento: evento.nome || evento.tipoLabel });

        botaoAceitarConvite.onclick = () => {
            Momentus.responderColaborador(evento.id, colaborador.id, 'ativo');
            mostrarToast(Momentus.t('conviteAceitoToast'));
            fecharModalConvite();
        };
        botaoRecusarConvite.onclick = () => {
            Momentus.responderColaborador(evento.id, colaborador.id, 'recusado');
            mostrarToast(Momentus.t('conviteRecusadoToast'));
            fecharModalConvite();
        };

        overlayConvite.classList.add('aberto');
    }
    if (fecharConviteBtn) fecharConviteBtn.addEventListener('click', fecharModalConvite);
    if (overlayConvite) {
        overlayConvite.addEventListener('click', (e) => {
            if (e.target === overlayConvite) fecharModalConvite();
        });
    }

    function renderizarTarefas(evento) {
        const tarefas = (evento.tarefas && evento.tarefas.length) ? evento.tarefas : Momentus.tarefasPadrao();
        const listaEl = container.querySelector('#listaTarefasEvento');
        listaEl.innerHTML = tarefas.map((tf) => `
            <div class="itemTarefaEvento ${tf.feita ? 'feita' : ''}" data-id="${tf.id}">
                <div class="checkTarefa"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M20 6 9 17l-5-5"/></svg></div>
                <span class="textoTarefa">${Momentus.t(tf.chave)}</span>
            </div>`).join('');
        listaEl.querySelectorAll('.itemTarefaEvento').forEach((el) => {
            el.addEventListener('click', () => {
                Momentus.alternarTarefa(evento.id, el.dataset.id);
            });
        });
    }

    // Espera a primeira sincronização com o backend antes de desenhar a
    // tela (senão o evento apareceria como "não encontrado" por um
    // instante enquanto a API ainda está respondendo).
    Momentus.aguardarEventosProntos().then(() => {
        renderizarEvento();
        verificarConviteNaUrl();
    });
    document.addEventListener('momentus:eventos-alterados', renderizarEvento);
    document.addEventListener('momentus:idioma-alterado', renderizarEvento);
})();
