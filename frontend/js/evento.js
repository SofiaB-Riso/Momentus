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
        const gasto = Number(evento.totalDespesas || 0);
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
        const botaoEditarEvento = container.querySelector('#botaoEditarEvento');
        const botaoApagarEvento = container.querySelector('#botaoApagarEvento');
        const podeEditarEvento = evento.permissao === 'dono' || evento.podeEditar !== false;
        if (podeEditarEvento) botaoEditarEvento.addEventListener('click', () => { window.location.href = 'planejar.html?id=' + encodeURIComponent(evento.id); });
        else botaoEditarEvento.style.display = 'none';
        if (evento.permissao === 'dono') {
            botaoApagarEvento.addEventListener('click', async () => {
                if (window.confirm(Momentus.t('confirmarApagarEvento', { nome: evento.nome || evento.tipoLabel }))) {
                    const removeu = await Momentus.removerEvento(evento.id);
                    if (removeu) window.location.href = 'eventos.html';
                }
            });
        } else botaoApagarEvento.style.display = 'none';

        renderizarConvidados(evento);
        renderizarColaboradores(evento);
        renderizarItensCompartilhados(evento);
        renderizarItens(evento);
        renderizarTarefas(evento);
        renderizarFinanceiro(evento);
        renderizarGaleria(evento);
        ligarRateio(evento);

        // Botão de adicionar colaborador (dentro do template, precisa ser religado a cada render)
        const botaoAddColab = container.querySelector('#botaoAdicionarColaborador');
        if (botaoAddColab) {
            if (evento.permissao !== 'dono') botaoAddColab.style.display = 'none';
            else botaoAddColab.addEventListener('click', () => abrirModalColaborador());
        }
        ligarFormularioItemCompartilhado(evento);

        // Formulário de convidado
        const formConvidado = container.querySelector('#formConvidado');
        formConvidado.addEventListener('submit', async (e) => {
            e.preventDefault();
            const nome = container.querySelector('#nomeNovoConvidado').value.trim();
            const contato = container.querySelector('#contatoNovoConvidado').value.trim();
            const restricoes = container.querySelector('#restricoesNovoConvidado').value.trim();
            if (!nome) return;
            const criado = await Momentus.adicionarConvidado(evento.id, { nome, contato, restricoes });
            if (criado) {
                container.querySelector('#nomeNovoConvidado').value = '';
                container.querySelector('#contatoNovoConvidado').value = '';
                container.querySelector('#restricoesNovoConvidado').value = '';
                if (criado.link_rsvp) mostrarToast('Convidado adicionado! O link de RSVP foi criado.');
            }
        });

        const privacidade = container.querySelector('#privacidadeListaConvidados');
        if (privacidade) {
            privacidade.value = evento.privacidadeConvidados || 'organizador';
            privacidade.disabled = evento.permissao !== 'dono';
            if (evento.permissao === 'dono') privacidade.addEventListener('change', () => Momentus.atualizarEvento(evento.id, { privacidadeConvidados: privacidade.value }));
        }
        if (!podeEditarEvento) {
            container.querySelectorAll('form').forEach((form) => { form.style.display = 'none'; });
            container.querySelectorAll('.botaoRemoverConvidado, .removerFotoEvento').forEach((b) => { b.style.display = 'none'; });
            container.querySelectorAll('.selectStatusConvidado').forEach((el) => { if (el.id !== 'privacidadeListaConvidados') el.disabled = true; });
        }

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
            const restr = raiz.querySelector('.restricoesConvidado');
            if (restr) restr.textContent = conv.restricoes ? 'Restrições: ' + conv.restricoes : '';
            const copiar = raiz.querySelector('.copiarRsvp');
            if (copiar) copiar.addEventListener('click', async () => {
                const link = new URL('rsvp.html?token=' + encodeURIComponent(conv.token_rsvp || ''), window.location.href).toString();
                try { await navigator.clipboard.writeText(link); mostrarToast('Link de RSVP copiado!'); }
                catch (_) { mostrarToast(link); }
            });
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
                botaoReenviar.addEventListener('click', async () => {
                    const atual = Momentus.reenviarConviteColaborador(evento.id, colab.id) || colab;
                    const link = construirLinkConvite(atual.token || colab.token);
                    const copiou = await copiarLink(link);
                    mostrarToast(copiou ? 'Link do convite copiado para reenviar.' : `Compartilhe este link: ${link}`);
                });
            }

            const botaoRemover = raiz.querySelector('.botaoRemoverConvidado');
            if (evento.permissao === 'dono') {
                const permissao = document.createElement('label');
                permissao.className = 'permissaoColaborador';
                permissao.innerHTML = `<input type="checkbox" ${colab.pode_editar !== false ? 'checked' : ''}><span>Pode editar</span>`;
                permissao.querySelector('input').addEventListener('change', (e) => Momentus.definirPermissaoColaborador(evento.id, colab.id, e.target.checked));
                raiz.insertBefore(permissao, botaoRemover);
                botaoRemover.addEventListener('click', () => {
                    if (window.confirm(Momentus.t('confirmarRemoverColaborador', { nome: colab.nome || '' }))) {
                        Momentus.removerColaborador(evento.id, colab.id);
                    }
                });
            } else {
                botaoRemover.style.display = 'none';
            }
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
            const resultado = await Momentus.adicionarItemCompartilhado(evento.id, { nome, quantidade: qtdInput.value });
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
        return new URL('convite.html?token=' + encodeURIComponent(token), window.location.href).toString();
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

            const colaborador = await Momentus.adicionarColaborador(evento.id, { nome, contato: email });
            if (!colaborador) return;

            const link = colaborador.link_convite ? new URL(colaborador.link_convite, window.location.href).toString() : construirLinkConvite(colaborador.token);

            if (modo === 'email') {
                const copiou = await copiarLink(link);
                const mensagem = colaborador.possui_conta
                    ? (copiou
                        ? 'Convite criado, notificação enviada no Momentus e link copiado.'
                        : `Convite criado e notificação enviada no Momentus. Compartilhe também: ${link}`)
                    : (copiou
                        ? 'Convite criado. Como essa pessoa ainda não tem conta, o link foi copiado para você compartilhar.'
                        : `Convite criado. Compartilhe este link com a pessoa: ${link}`);
                mostrarToast(mensagem);
                fecharModalColaborador();
            } else {
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
        listaEl.innerHTML = tarefas.map((tf) => {
            const texto = tf.chave ? Momentus.t(tf.chave) : (tf.titulo || 'Tarefa');
            const prazo = tf.prazo ? `<small style="margin-left:auto;color:var(--tinta-suave);">${new Date(tf.prazo).toLocaleString('pt-BR')}</small>` : '';
            return `
            <div class="itemTarefaEvento ${tf.feita ? 'feita' : ''}" data-id="${tf.id}">
                <div class="checkTarefa"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M20 6 9 17l-5-5"/></svg></div>
                <span class="textoTarefa">${escapeHTML(texto)}</span>${prazo}
            </div>`;
        }).join('');
        listaEl.querySelectorAll('.itemTarefaEvento').forEach((el) => {
            el.addEventListener('click', () => Momentus.alternarTarefa(evento.id, el.dataset.id));
        });

        const form = container.querySelector('#formNovaTarefa');
        if (form) form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const titulo = container.querySelector('#tituloNovaTarefa').value.trim();
            const prazo = container.querySelector('#prazoNovaTarefa').value;
            if (!titulo) return;
            await Momentus.adicionarTarefa(evento.id, { titulo, prazo: prazo || null });
        });
    }

    function renderizarFinanceiro(evento) {
        const orcamento = Number(evento.orcamento || 0);
        const total = Number(evento.totalDespesas || 0);
        const restante = orcamento - total;
        const finOrcamento = container.querySelector('#finOrcamento');
        if (!finOrcamento) return;
        finOrcamento.textContent = formatarMoeda(orcamento);
        container.querySelector('#finGasto').textContent = formatarMoeda(total);
        container.querySelector('#finRestante').textContent = formatarMoeda(restante);
        const situacao = container.querySelector('#finSituacao');
        situacao.textContent = orcamento > 0 && total > orcamento ? 'Orçamento ultrapassado' : 'Dentro do orçamento';
        situacao.style.color = orcamento > 0 && total > orcamento ? '#d64545' : '';

        const lista = container.querySelector('#listaDespesasEvento');
        const despesas = evento.despesas || [];
        lista.innerHTML = despesas.length ? despesas.map((d) => `
            <div class="linhaItemEvento" data-despesa="${d.id}">
                <div class="thumbItemEvento" style="background:var(--grad-1)"></div>
                <div style="flex:1;min-width:0;"><strong>${escapeHTML(d.descricao)}</strong><div class="metaItemEvento">${escapeHTML(d.categoria || 'geral')} · ${escapeHTML(d.pago_por || '')}${d.comprovante_url ? ` · <a href="${escapeHTML(d.comprovante_url)}" target="_blank" rel="noopener">ver comprovante</a>` : ''}</div></div>
                <span class="precoItemEvento">${formatarMoeda(Number(d.valor || 0))}</span>
                <button type="button" class="botaoRemoverConvidado removerDespesa" aria-label="Remover despesa">×</button>
            </div>`).join('') : '<p class="estadoVazioClaro" style="text-align:left;padding-left:0;">Nenhuma despesa real registrada.</p>';
        lista.querySelectorAll('.removerDespesa').forEach((btn) => btn.addEventListener('click', async () => {
            const linha = btn.closest('[data-despesa]');
            await Momentus.removerDespesa(evento.id, linha.dataset.despesa);
        }));

        const form = container.querySelector('#formDespesaEvento');
        if (form) form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const descricao = container.querySelector('#descDespesaEvento').value.trim();
            const categoria = container.querySelector('#categoriaDespesaEvento').value.trim();
            const valor = Number(container.querySelector('#valorDespesaEvento').value || 0);
            const inputComprovante = container.querySelector('#comprovanteDespesaEvento');
            if (!descricao || valor <= 0) return;
            const criado = await Momentus.adicionarDespesa(evento.id, { descricao, categoria, valor });
            const despesaId = criado && criado.despesa ? criado.despesa.id : (criado && criado.id);
            if (despesaId && inputComprovante && inputComprovante.files && inputComprovante.files[0]) {
                await Momentus.enviarComprovanteDespesa(evento.id, despesaId, inputComprovante.files[0]);
            }
        });

        const pdf = container.querySelector('#baixarPdfEvento');
        const xlsx = container.querySelector('#baixarExcelEvento');
        if (pdf) pdf.href = `/eventos/${encodeURIComponent(evento.id)}/relatorio.pdf`;
        if (xlsx) xlsx.href = `/eventos/${encodeURIComponent(evento.id)}/relatorio.xlsx`;

        const inteligente = container.querySelector('#resumoInteligenteEvento');
        if (inteligente) {
            inteligente.innerHTML = '<p class="estadoVazioClaro" style="text-align:left;padding-left:0;">Calculando sugestões...</p>';
            Momentus.obterResumoEvento(evento.id).then((resumo) => {
                if (!resumo || !container.querySelector('#resumoInteligenteEvento')) return;
                const s = resumo.suprimentos || {};
                const restricoes = (resumo.convidados && resumo.convidados.restricoes_alimentares) || [];
                const fornecedores = resumo.fornecedores_recomendados || [];
                const locais = resumo.locais_recomendados || [];
                const ob = resumo.orcamento_base || {};
                inteligente.innerHTML = `
                    <div class="grelhaInfoEvento">
                        <div class="blocoInfoEvento"><div class="rotuloInfo">Pessoas consideradas</div><div class="valorInfo">${s.pessoas_consideradas || 0}</div></div>
                        <div class="blocoInfoEvento"><div class="rotuloInfo">Comida sugerida</div><div class="valorInfo">${s.comida_kg || 0} kg</div></div>
                        <div class="blocoInfoEvento"><div class="rotuloInfo">Bebidas sugeridas</div><div class="valorInfo">${s.bebidas_litros || 0} L</div></div>
                        <div class="blocoInfoEvento"><div class="rotuloInfo">Doces sugeridos</div><div class="valorInfo">${s.doces_unidades || 0} un.</div></div>
                    </div>
                    <div style="margin-top:1rem;"><strong>Estimativa de orçamento base:</strong><div class="chipsSugestao" style="margin-top:.6rem;"><span>Alimentação ${formatarMoeda(ob.alimentacao || 0)}</span><span>Bebidas ${formatarMoeda(ob.bebidas || 0)}</span><span>Decoração ${formatarMoeda(ob.decoracao || 0)}</span><span>Local ${formatarMoeda(ob.local || 0)}</span><span><b>Total ${formatarMoeda(ob.total_estimado || 0)}</b></span></div></div>
                    <p style="margin-top:1rem;"><strong>Restrições alimentares:</strong> ${restricoes.length ? restricoes.map(escapeHTML).join(', ') : 'nenhuma informada'}</p>
                    <p style="margin-top:.7rem;"><a class="botaoSecundario" target="_blank" rel="noopener" href="${escapeHTML(resumo.mapa_url || '#')}">Abrir local no mapa</a></p>
                    ${locais.length ? `<div style="margin-top:1rem;"><strong>Espaços sugeridos${evento.cidade ? ` em ${escapeHTML(evento.cidade)}` : ''}:</strong><div class="chipsSugestao" style="margin-top:.6rem;">${locais.map((f) => `<span>${escapeHTML(f.nome_empresa)} · ★ ${Number(f.avaliacao || 0).toFixed(1)}</span>`).join('')}</div></div>` : ''}
                    ${fornecedores.length ? `<div style="margin-top:1rem;"><strong>Fornecedores recomendados:</strong><div class="chipsSugestao" style="margin-top:.6rem;">${fornecedores.map((f) => `<span>${escapeHTML(f.nome_empresa)} · ${escapeHTML(f.tipo_servico)}</span>`).join('')}</div></div>` : ''}`;
            });
        }
    }

    function renderizarGaleria(evento) {
        const galeria = container.querySelector('#galeriaEvento');
        if (!galeria) return;
        const fotos = evento.fotos || [];
        galeria.innerHTML = fotos.length ? fotos.map((f) => `
            <figure class="fotoGaleriaMomentus" data-foto="${f.id}">
                <img src="${escapeHTML(f.url || '')}" alt="${escapeHTML(f.legenda || 'Foto do evento')}">
                <figcaption>${escapeHTML(f.legenda || '')}<button type="button" class="removerFotoEvento" aria-label="Remover foto">×</button></figcaption>
            </figure>`).join('') : '<p class="estadoVazioClaro" style="grid-column:1/-1;text-align:left;padding-left:0;">A galeria ainda está vazia.</p>';
        galeria.querySelectorAll('.removerFotoEvento').forEach((btn) => btn.addEventListener('click', async () => {
            await Momentus.removerFoto(evento.id, btn.closest('[data-foto]').dataset.foto);
        }));

        const form = container.querySelector('#formFotoEvento');
        if (form) form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const input = container.querySelector('#arquivoFotoEvento');
            const legenda = container.querySelector('#legendaFotoEvento').value.trim();
            if (!input.files || !input.files[0]) return;
            await Momentus.enviarFoto(evento.id, input.files[0], legenda);
        });
    }

    Momentus.aguardarEventosProntos().then(() => {
        renderizarEvento();
        verificarConviteNaUrl();
    });
    document.addEventListener('momentus:eventos-alterados', renderizarEvento);
    document.addEventListener('momentus:idioma-alterado', renderizarEvento);
})();
