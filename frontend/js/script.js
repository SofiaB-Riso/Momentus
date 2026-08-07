/* ================= MENU LATERAL (ativo ao clicar) ================= */
const itensMenu = document.querySelectorAll('.item');

/* ================= HAMBÚRGUER (tablet/celular) ================= */
const botaoMenu = document.getElementById('botaoMenu');
const menuLateral = document.querySelector('.menulateral');
const overlayMenu = document.getElementById('overlayMenu');

function alternarMenu() {
    botaoMenu.classList.toggle('aberto');
    menuLateral.classList.toggle('aberto');
    overlayMenu.classList.toggle('aberto');
    const aberto = menuLateral.classList.contains('aberto');
    botaoMenu.setAttribute('aria-expanded', aberto);
}

function fecharMenu() {
    botaoMenu.classList.remove('aberto');
    menuLateral.classList.remove('aberto');
    overlayMenu.classList.remove('aberto');
    botaoMenu.setAttribute('aria-expanded', 'false');
}

if (botaoMenu) {
    botaoMenu.addEventListener('click', alternarMenu);
    overlayMenu.addEventListener('click', fecharMenu);
    itensMenu.forEach((item) => item.addEventListener('click', fecharMenu));
}

/* ================= FORMATAÇÃO AUXILIAR ================= */

function formatarMoeda(valor) {
    const idioma = Momentus.obterIdioma();
    const locale = idioma === 'en' ? 'en-US' : idioma === 'es' ? 'es-ES' : 'pt-BR';
    return 'R$ ' + Number(valor || 0).toLocaleString(locale);
}

function formatarDataBR(valorISO) {
    if (!valorISO) return '—';
    const [ano, mes, dia] = valorISO.split('-');
    return `${dia}/${mes}/${ano}`;
}

const STATUS_LABEL_CHAVE = {
    confirmado: 'statusConfirmado',
    planejamento: 'statusPlanejamento',
    agendado: 'statusAgendado',
    rascunho: 'statusRascunho'
};

const TIPO_EMOJI = {
    aniversario: '🎂', casamento: '💍', churrasco: '🍖',
    formatura: '🎓', corporativo: '🏢', chadebebe: '👶'
};

/* ================= TOAST GLOBAL ================= */
let _toastTimeout = null;
function mostrarToast(texto) {
    const toast = document.getElementById('toastMomentus');
    if (!toast) return;
    const span = document.getElementById('toastTexto');
    if (span) span.textContent = texto;
    toast.classList.add('visivel');
    clearTimeout(_toastTimeout);
    _toastTimeout = setTimeout(() => toast.classList.remove('visivel'), 2600);
}

/* ================= PÁGINA INÍCIO: eventos, calendário e estatísticas ================= */

const gradeCalendario = document.getElementById('calendarioGrid');

if (gradeCalendario) {

    let mesAtual = 3;   // Abril (0-index) — mês em destaque no protótipo
    let anoAtual = 2026;
    let mesInicializado = false;
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);

    function eventosOrdenados() {
        return Momentus.obterEventos().slice().sort((a, b) => (a.data + a.hora).localeCompare(b.data + b.hora));
    }

    function proximoEvento() {
        const futuros = eventosOrdenados().filter((ev) => Momentus.diasEntre(ev.data) >= 0);
        if (futuros.length) return futuros[0];
        const todos = eventosOrdenados();
        return todos.length ? todos[todos.length - 1] : null;
    }

    function renderizarCabecalho() {
        const eventos = Momentus.obterEventos();
        const totalStr = document.getElementById('subtituloEventos');
        if (totalStr) {
            const n = eventos.length;
            if (n === 0) totalStr.textContent = Momentus.t('iniSubtitulo0');
            else if (n === 1) totalStr.textContent = Momentus.t('iniSubtitulo1');
            else totalStr.textContent = Momentus.t('iniSubtituloN', { n });
        }
        const tituloOla = document.getElementById('tituloOla');
        if (tituloOla) {
            const perfil = Momentus.obterPerfil();
            const primeiroNome = perfil.nome.split(' ')[0];
            tituloOla.textContent = Momentus.t('iniOla', { nome: primeiroNome });
        }
    }

    function renderizarCardIngresso() {
        const container = document.getElementById('cardProximoEvento');
        if (!container) return;
        const evento = proximoEvento();

        if (!evento) {
            container.classList.add('cardIngresso');
            container.innerHTML = `
                <div class="corpoIngresso" style="border-radius:var(--raio);">
                    <div class="estadoVazio">
                        <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><path d="M12 2 4 7v10l8 5 8-5V7l-8-5Z"/><path d="M4 7l8 5 8-5"/><path d="M12 22V12"/></svg>
                        <strong>${Momentus.t('semEventoTitulo')}</strong>
                        <span>${Momentus.t('semEventoTexto')}</span>
                    </div>
                </div>`;
            return;
        }

        const dias = Momentus.diasEntre(evento.criadoEm ? evento.criadoEm.slice(0, 10) : evento.data);
        const diasDesdeCriacao = Math.max(0, Math.round((hoje - new Date((evento.criadoEm || evento.data).slice(0, 10) + 'T00:00:00')) / 86400000));
        const dataObj = new Date(evento.data + 'T00:00:00');
        const meses = Momentus.obterMesesAbrev();

        container.innerHTML = `
            <div class="corpoIngresso">
                <div class="cabecalhoCard">
                    <div>
                        <span class="tagCard">${Momentus.t('proximoEvento')}</span>
                        <div class="nomeEvento">${escapeHTML(evento.nome || evento.tipoLabel)}</div>
                    </div>
                </div>
                <div class="infoEvento">
                    <div class="linhaInfo">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                        ${escapeHTML(evento.local || '—')}
                    </div>
                    <div class="linhaInfo">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                        ${formatarDataBR(evento.data)} · ${diasDesdeCriacao > 0 ? Momentus.t('ultimaAlteracao', { n: diasDesdeCriacao }) : Momentus.t('criadoAgora')}
                    </div>
                </div>
                <div class="barraProgresso">
                    <div class="rotulo"><span>${Momentus.t('preparativos')}</span><span>${evento.progresso || 0}%</span></div>
                    <div class="trilhaProgresso"><div class="preenchimentoProgresso" style="width:${evento.progresso || 0}%"></div></div>
                </div>
            </div>
            <div class="canhotoIngresso">
                <span class="numeroCanhoto">Nº ${String(evento.numero || 1).padStart(3, '0')}</span>
                <div class="setaCard">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                </div>
                <span class="dataCanhoto">${dataObj.getDate()}<br>${meses[dataObj.getMonth()]}</span>
            </div>`;
        container.style.cursor = 'pointer';
        container.onclick = () => { window.location.href = 'evento.html?id=' + encodeURIComponent(evento.id); };
    }

    function classeGrupo(indice) {
        return ['g1', 'g2', 'g3'][indice % 3];
    }

    function renderizarListaProximos() {
        const lista = document.getElementById('listaProximosEventos');
        if (!lista) return;
        const proximos = eventosOrdenados().filter((ev) => Momentus.diasEntre(ev.data) >= -1).slice(0, 4);

        if (!proximos.length) {
            lista.innerHTML = `<p class="estadoVazioClaro" style="text-align:left; padding-left:0;">${Momentus.t('semProximos')}</p>`;
            return;
        }

        const meses = Momentus.obterMesesAbrev();
        lista.innerHTML = proximos.map((ev, i) => {
            const d = new Date(ev.data + 'T00:00:00');
            const statusChave = STATUS_LABEL_CHAVE[ev.status] || 'statusAgendado';
            return `
            <div class="itemProximo" data-id="${ev.id}" style="cursor:pointer;">
                <div class="badgeData ${classeGrupo(i)}">${d.getDate()} ${meses[d.getMonth()]}</div>
                <div class="detalhesProximo">
                    <div class="nomeItem">${escapeHTML(ev.nome || ev.tipoLabel)}</div>
                    <div class="subItem">${escapeHTML(ev.local || '—')} · ${escapeHTML(ev.hora || '')}</div>
                </div>
                <span class="statusPill">${Momentus.t(statusChave)}</span>
            </div>`;
        }).join('');
        lista.querySelectorAll('.itemProximo').forEach((el) => {
            el.addEventListener('click', () => { window.location.href = 'evento.html?id=' + encodeURIComponent(el.dataset.id); });
        });
    }

    function renderizarEstatisticas() {
        const eventos = Momentus.obterEventos();
        const totalConvidados = eventos.reduce((soma, ev) => soma + (Number(ev.convidados) || 0), 0);
        const totalOrcamento = eventos.reduce((soma, ev) => soma + (Number(ev.orcamento) || 0), 0);
        const prox = proximoEvento();
        const dias = prox ? Math.max(0, Momentus.diasEntre(prox.data)) : 0;

        definirContador('statEventos', eventos.length);
        definirContador('statConvidados', totalConvidados);
        definirContador('statDias', dias);
        definirContador('statOrcamento', totalOrcamento, 'R$ ');
    }

    function definirContador(id, valor, prefixo) {
        const el = document.getElementById(id);
        if (!el) return;
        el.dataset.count = valor;
        if (prefixo) el.dataset.prefix = prefixo;
        el.textContent = (prefixo || '') + '0';
        animarNumero(el);
    }

    function renderizarCalendario() {
        gradeCalendario.innerHTML = '';
        const meses = Momentus.obterMeses();
        document.getElementById('mesAnoAtual').textContent = `${meses[mesAtual]} ${anoAtual}`;

        const eventosCalendario = {};
        Momentus.obterEventos().forEach((ev, i) => {
            const [a, m, d] = ev.data.split('-').map(Number);
            const chave = `${a}-${m - 1}-${d}`;
            eventosCalendario[chave] = classeGrupo(i) === 'g2' ? 'evento2' : 'evento';
        });

        const primeiroDiaSemana = new Date(anoAtual, mesAtual, 1).getDay();
        const totalDias = new Date(anoAtual, mesAtual + 1, 0).getDate();
        const diasMesAnterior = new Date(anoAtual, mesAtual, 0).getDate();

        for (let i = primeiroDiaSemana - 1; i >= 0; i--) {
            const el = document.createElement('div');
            el.className = 'dia fora';
            el.textContent = diasMesAnterior - i;
            gradeCalendario.appendChild(el);
        }

        for (let dia = 1; dia <= totalDias; dia++) {
            const el = document.createElement('div');
            el.className = 'dia';
            el.textContent = dia;

            const chave = `${anoAtual}-${mesAtual}-${dia}`;
            if (eventosCalendario[chave]) {
                el.classList.add(eventosCalendario[chave]);
            }

            if (dia === hoje.getDate() && mesAtual === hoje.getMonth() && anoAtual === hoje.getFullYear()) {
                el.classList.add('hoje');
            }

            gradeCalendario.appendChild(el);
        }

        const totalCelulas = primeiroDiaSemana + totalDias;
        const restante = (7 - (totalCelulas % 7)) % 7;
        for (let i = 1; i <= restante; i++) {
            const el = document.createElement('div');
            el.className = 'dia fora';
            el.textContent = i;
            gradeCalendario.appendChild(el);
        }
    }

    function renderizarTudoInicio() {
        renderizarCabecalho();
        renderizarCardIngresso();
        renderizarListaProximos();
        renderizarEstatisticas();
        renderizarCalendario();
    }

    document.getElementById('mesAnterior').addEventListener('click', () => {
        mesAtual--;
        if (mesAtual < 0) { mesAtual = 11; anoAtual--; }
        renderizarCalendario();
    });

    document.getElementById('mesProximo').addEventListener('click', () => {
        mesAtual++;
        if (mesAtual > 11) { mesAtual = 0; anoAtual++; }
        renderizarCalendario();
    });

    Momentus.aguardarEventosProntos().then(() => {

        const prox0 = proximoEvento();
        if (prox0) {
            const [a, m] = prox0.data.split('-').map(Number);
            anoAtual = a; mesAtual = m - 1;
        }
        renderizarTudoInicio();
    });

    document.addEventListener('momentus:eventos-alterados', renderizarTudoInicio);
    document.addEventListener('momentus:idioma-alterado', renderizarTudoInicio);
    document.addEventListener('momentus:perfil-alterado', renderizarCabecalho);
}

function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = String(str == null ? '' : str);
    return div.innerHTML;
}

/* ================= BUSCA NO CATÁLOGO (início) ================= */
const filtroCatalogoInicio = document.getElementById('filtroCatalogoInicio');
if (filtroCatalogoInicio) {
    filtroCatalogoInicio.addEventListener('input', (e) => {
        const termo = e.target.value.toLowerCase();
        document.querySelectorAll('#listaCatalogoInicio .itemCatalogo').forEach((item) => {
            const nome = item.querySelector('.nomeCatalogo').textContent.toLowerCase();
            item.style.display = nome.includes(termo) ? 'flex' : 'none';
        });
    });
}

/* ================= CATEGORIAS - PLANEJAR EVENTO ================= */
const CATEGORIA_LABEL_CHAVE = {
    aniversario: 'catAniversario', casamento: 'catCasamento', churrasco: 'catChurrasco',
    formatura: 'catFormatura', corporativo: 'catCorporativo', chadebebe: 'catChaBebe'
};

let tipoSelecionado = 'aniversario';

document.querySelectorAll('.chipCategoria').forEach((chip) => {
    chip.addEventListener('click', () => {
        document.querySelectorAll('.chipCategoria').forEach((c) => c.classList.remove('selecionado'));
        chip.classList.add('selecionado');
        tipoSelecionado = chip.dataset.tipo || 'aniversario';
        const resumoTipo = document.getElementById('resumoTipo');
        if (resumoTipo) resumoTipo.textContent = Momentus.t(CATEGORIA_LABEL_CHAVE[tipoSelecionado] || 'catAniversario');
    });
});

/* ================= RESUMO AO VIVO + SALVAR - PLANEJAR EVENTO ================= */
const formPlanejar = document.getElementById('formPlanejar');
if (formPlanejar) {
    (async () => {
    await Momentus.aguardarEventosProntos();

    const paramsPlanejar = new URLSearchParams(window.location.search);
    const idEdicao = paramsPlanejar.get('id');
    const eventoEmEdicao = idEdicao ? Momentus.obterEvento(idEdicao) : null;

    const nomeEvento = document.getElementById('nomeEvento');
    const dataEvento = document.getElementById('dataEvento');
    const horaEvento = document.getElementById('horaEvento');
    const localEvento = document.getElementById('localEvento');
    const convidados = document.getElementById('convidados');
    const estiloEvento = document.getElementById('estiloEvento');
    const observacoes = document.getElementById('observacoes');
    const orcamento = document.getElementById('orcamento');
    const valorOrcamento = document.getElementById('valorOrcamento');
    const resumoTipo = document.getElementById('resumoTipo');

    if (resumoTipo) resumoTipo.textContent = Momentus.t('catAniversario');

    // Sugere uma data padrão a partir de hoje (em vez de uma data fixa do protótipo)
    (function sugerirDataPadrao() {
        const d = new Date();
        d.setDate(d.getDate() + 14);
        dataEvento.value = d.toISOString().slice(0, 10);
        document.getElementById('resumoData').textContent = formatarDataBR(dataEvento.value);
    })();

    // Modo edição: pré-preenche o formulário com os dados do evento existente
    if (eventoEmEdicao) {
        const eyebrow = document.getElementById('eyebrowPlanejar');
        const titulo = document.getElementById('tituloPlanejar');
        if (eyebrow) eyebrow.textContent = Momentus.t('editarEventoTitulo');
        if (titulo) titulo.textContent = eventoEmEdicao.nome || eventoEmEdicao.tipoLabel;

        document.querySelectorAll('.chipCategoria').forEach((chip) => {
            chip.classList.toggle('selecionado', chip.dataset.tipo === eventoEmEdicao.tipo);
        });
        tipoSelecionado = eventoEmEdicao.tipo || 'aniversario';

        nomeEvento.value = eventoEmEdicao.nome || '';
        dataEvento.value = eventoEmEdicao.data || dataEvento.value;
        horaEvento.value = eventoEmEdicao.hora && eventoEmEdicao.hora !== '—' ? eventoEmEdicao.hora : '';
        localEvento.value = eventoEmEdicao.local || '';
        convidados.value = eventoEmEdicao.convidados || '';
        if (eventoEmEdicao.estilo) {
            const opcoes = Array.from(estiloEvento.options);
            const encontrada = opcoes.find((op) => op.textContent.trim() === eventoEmEdicao.estilo);
            if (encontrada) estiloEvento.value = encontrada.value;
        }
        orcamento.value = eventoEmEdicao.orcamento || orcamento.value;
        observacoes.value = eventoEmEdicao.observacoes || '';

        document.getElementById('resumoTipo').textContent = Momentus.t(CATEGORIA_LABEL_CHAVE[tipoSelecionado] || 'catAniversario');
        document.getElementById('resumoNome').textContent = nomeEvento.value || '—';
        document.getElementById('resumoData').textContent = formatarDataBR(dataEvento.value);
        document.getElementById('resumoConvidados').textContent = convidados.value ? `${convidados.value} ${Momentus.t('resumoConvidadosSufixo')}` : '—';

        const botaoSalvarSpan = formPlanejar.querySelector('.botaoPrimario span');
        if (botaoSalvarSpan) botaoSalvarSpan.textContent = Momentus.t('salvarAlteracoesEvento');
        const botaoRascunhoEl = document.getElementById('botaoRascunho');
        if (botaoRascunhoEl) botaoRascunhoEl.style.display = 'none';
    }

    nomeEvento.addEventListener('input', () => {
        document.getElementById('resumoNome').textContent = nomeEvento.value || '—';
    });

    dataEvento.addEventListener('input', () => {
        document.getElementById('resumoData').textContent = formatarDataBR(dataEvento.value);
    });

    convidados.addEventListener('input', () => {
        document.getElementById('resumoConvidados').textContent = convidados.value ? `${convidados.value} ${Momentus.t('resumoConvidadosSufixo')}` : '—';
    });

    function atualizarSliderOrcamento() {
        const min = Number(orcamento.min), max = Number(orcamento.max), val = Number(orcamento.value);
        const pct = ((val - min) / (max - min)) * 100;
        orcamento.style.background = `linear-gradient(90deg, #7c5cff ${pct}%, var(--linha) ${pct}%)`;
        valorOrcamento.textContent = formatarMoeda(val);
        document.getElementById('resumoOrcamento').textContent = formatarMoeda(val);
    }
    orcamento.addEventListener('input', atualizarSliderOrcamento);
    atualizarSliderOrcamento();

    function montarEventoDoFormulario(status) {
        return {
            tipo: tipoSelecionado,
            tipoLabel: Momentus.t(CATEGORIA_LABEL_CHAVE[tipoSelecionado] || 'catAniversario'),
            nome: nomeEvento.value.trim() || Momentus.t(CATEGORIA_LABEL_CHAVE[tipoSelecionado] || 'catAniversario'),
            data: dataEvento.value || new Date().toISOString().slice(0, 10),
            hora: horaEvento.value.trim() || '—',
            local: localEvento.value.trim(),
            convidados: Number(convidados.value) || 0,
            estilo: estiloEvento.value,
            orcamento: Number(orcamento.value) || 0,
            observacoes: observacoes.value.trim(),
            status: status,
            progresso: status === 'rascunho' ? 5 : 20
        };
    }

    formPlanejar.addEventListener('submit', async (e) => {
        e.preventDefault();
        const botao = formPlanejar.querySelector('.botaoPrimario');
        const textoOriginalBotao = botao.innerHTML;

        if (eventoEmEdicao) {
            const dadosAtualizados = montarEventoDoFormulario(eventoEmEdicao.status);
            dadosAtualizados.progresso = eventoEmEdicao.progresso || 0;
            const resultado = await Momentus.atualizarEvento(eventoEmEdicao.id, dadosAtualizados);
            if (!resultado) { botao.innerHTML = textoOriginalBotao; return; }
            botao.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg> ${Momentus.t('alteracoesSalvasEvento')}`;
            setTimeout(() => { window.location.href = 'evento.html?id=' + encodeURIComponent(eventoEmEdicao.id); }, 700);
            return;
        }

        const criado = await Momentus.salvarEvento(montarEventoDoFormulario('confirmado'));
        if (!criado) { botao.innerHTML = textoOriginalBotao; return; }
        botao.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg> ${Momentus.t('botaoSalvarEventoOk')}`;
        setTimeout(() => { window.location.href = 'inicio.html'; }, 900);
    });

    const botaoRascunho = document.getElementById('botaoRascunho');
    if (botaoRascunho && !eventoEmEdicao) {
        botaoRascunho.addEventListener('click', async () => {
            const criado = await Momentus.salvarEvento(montarEventoDoFormulario('rascunho'));
            if (!criado) return;
            botaoRascunho.textContent = Momentus.t('botaoRascunhoOk');
            setTimeout(() => { window.location.href = 'inicio.html'; }, 900);
        });
    }
    })();
}

/* ================= FILTROS - CATÁLOGO ================= */
const filtrosCatalogo = document.querySelectorAll('.filtroChip');
if (filtrosCatalogo.length) {
    const cardsProduto = document.querySelectorAll('.cardProduto');

    function aplicarFiltroAtivo() {
        const filtroAtivo = document.querySelector('.filtroChip.ativoFiltro');
        const categoria = filtroAtivo ? filtroAtivo.dataset.filtro : 'todos';
        cardsProduto.forEach((card) => {
            let mostrar = true;
            if (categoria === 'favoritos') {
                mostrar = Momentus.ehFavorito(card.dataset.nome);
            } else if (categoria !== 'todos') {
                mostrar = card.dataset.categoria === categoria;
            }
            card.style.display = mostrar ? 'flex' : 'none';
        });
        const semResultado = Array.from(cardsProduto).every((c) => c.style.display === 'none');
        let avisoVazio = document.getElementById('avisoCatalogoVazio');
        if (categoria === 'favoritos' && semResultado) {
            if (!avisoVazio) {
                avisoVazio = document.createElement('p');
                avisoVazio.id = 'avisoCatalogoVazio';
                avisoVazio.className = 'estadoVazioClaro';
                avisoVazio.style.gridColumn = '1 / -1';
                document.getElementById('grelhaCatalogo').appendChild(avisoVazio);
            }
            avisoVazio.textContent = Momentus.t('nenhumFavorito');
        } else if (avisoVazio) {
            avisoVazio.remove();
        }
    }

    filtrosCatalogo.forEach((filtro) => {
        filtro.addEventListener('click', () => {
            filtrosCatalogo.forEach((f) => f.classList.remove('ativoFiltro'));
            filtro.classList.add('ativoFiltro');
            aplicarFiltroAtivo();
        });
    });

    const buscaCatalogoGeral = document.getElementById('buscaCatalogoGeral');
    if (buscaCatalogoGeral) {
        buscaCatalogoGeral.addEventListener('input', (e) => {
            const termo = e.target.value.toLowerCase();
            filtrosCatalogo.forEach((f) => f.classList.remove('ativoFiltro'));
            document.querySelector('[data-filtro="todos"]').classList.add('ativoFiltro');
            cardsProduto.forEach((card) => {
                const nome = card.dataset.nome || '';
                card.style.display = nome.includes(termo) ? 'flex' : 'none';
            });
            const avisoVazio = document.getElementById('avisoCatalogoVazio');
            if (avisoVazio) avisoVazio.remove();
        });
    }

    document.addEventListener('momentus:favoritos-alterados', aplicarFiltroAtivo);
    document.addEventListener('momentus:idioma-alterado', aplicarFiltroAtivo);

    /* ---- Favoritar produtos ---- */
    document.querySelectorAll('.tagFavorito').forEach((botao) => {
        const card = botao.closest('.cardProduto');
        const produtoId = card ? card.dataset.nome : null;
        if (produtoId && Momentus.ehFavorito(produtoId)) botao.classList.add('favoritado');

        botao.addEventListener('click', () => {
            if (!produtoId) return;
            Momentus.alternarFavorito(produtoId);
            botao.classList.toggle('favoritado');
        });
    });

    /* ---- Adicionar item do catálogo a um evento (popup) ---- */
    const overlayEscolherEvento = document.getElementById('overlayEscolherEvento');
    if (overlayEscolherEvento) {
        const corpoEscolher = document.getElementById('corpoEscolherEvento');
        const textoEscolher = document.getElementById('textoEscolherEvento');
        const fecharBtn = document.getElementById('fecharEscolherEvento');
        let produtoSelecionado = null;

        function fecharModalEscolha() {
            overlayEscolherEvento.classList.remove('aberto');
            produtoSelecionado = null;
        }

        fecharBtn.addEventListener('click', fecharModalEscolha);
        overlayEscolherEvento.addEventListener('click', (e) => {
            if (e.target === overlayEscolherEvento) fecharModalEscolha();
        });

        function abrirModalEscolha(produto) {
            produtoSelecionado = produto;
            textoEscolher.textContent = Momentus.t('escolherEventoTexto', { produto: produto.nome });
            const eventos = Momentus.obterEventos();

            if (!eventos.length) {
                corpoEscolher.innerHTML = `
                    <div class="estadoVazioModal">
                        <p><strong>${Momentus.t('semEventosParaAdicionarTitulo')}</strong><br>${Momentus.t('semEventosParaAdicionarTexto')}</p>
                        <a href="planejar.html" class="botaoPrimario">${Momentus.t('criarEventoAgora')}</a>
                    </div>`;
            } else {
                corpoEscolher.innerHTML = `<div class="listaEscolhaEvento">${eventos.map((ev) => `
                    <button type="button" class="opcaoEscolhaEvento" data-id="${ev.id}">
                        <span class="emojiEscolhaEvento">${TIPO_EMOJI[ev.tipo] || '✨'}</span>
                        <span class="textoEscolhaEvento">
                            <span class="nomeEscolha">${escapeHTML(ev.nome || ev.tipoLabel)}</span>
                            <span class="subEscolha">${formatarDataBR(ev.data)} · ${escapeHTML(ev.local || '—')}</span>
                        </span>
                    </button>`).join('')}</div>`;

                corpoEscolher.querySelectorAll('.opcaoEscolhaEvento').forEach((opcao) => {
                    opcao.addEventListener('click', () => {
                        const evento = Momentus.obterEvento(opcao.dataset.id);
                        Momentus.adicionarItemCatalogo(opcao.dataset.id, produtoSelecionado);
                        mostrarToast(Momentus.t('itemAdicionadoEvento', { evento: evento ? (evento.nome || evento.tipoLabel) : '' }));
                        fecharModalEscolha();
                    });
                });
            }

            overlayEscolherEvento.classList.add('aberto');
        }

        document.querySelectorAll('.botaoAdicionar').forEach((botao) => {
            botao.addEventListener('click', () => {
                const card = botao.closest('.cardProduto');
                if (!card) return;
                const produto = {
                    produtoId: card.dataset.nome,
                    nome: card.querySelector('.nomeProduto') ? card.querySelector('.nomeProduto').textContent.trim() : card.dataset.nome,
                    categoria: card.dataset.categoria,
                    preco: Number(card.dataset.preco) || 0
                };
                botao.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6 9 17l-5-5"/></svg>';
                setTimeout(() => {
                    botao.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>';
                }, 1400);
                abrirModalEscolha(produto);
            });
        });
    }
}

/* ================= CONFIGURAÇÕES: perfil e preferências ================= */
const formPerfil = document.getElementById('formPerfil');
if (formPerfil) {
    const nomeConfig = document.getElementById('nomeConfig');
    const emailConfig = document.getElementById('emailConfig');
    const telefoneConfig = document.getElementById('telefoneConfig');
    const nomeGrandeConfig = document.getElementById('nomeGrandeConfig');
    const emailGrandeConfig = document.getElementById('emailGrandeConfig');
    const avatarGrandeConfig = document.getElementById('avatarGrandeConfig');

    function carregarPerfilNoFormulario() {
        const perfil = Momentus.obterPerfil();
        nomeConfig.value = perfil.nome;
        emailConfig.value = perfil.email;
        telefoneConfig.value = perfil.telefone;
        nomeGrandeConfig.textContent = perfil.nome;
        emailGrandeConfig.textContent = perfil.email;
        if (avatarGrandeConfig.firstChild && avatarGrandeConfig.firstChild.nodeType === 3) {
            avatarGrandeConfig.firstChild.textContent = Momentus.iniciais(perfil.nome) + ' ';
        }
    }
    carregarPerfilNoFormulario();

    formPerfil.addEventListener('submit', (e) => {
        e.preventDefault();
        Momentus.salvarPerfil({ nome: nomeConfig.value.trim(), email: emailConfig.value.trim(), telefone: telefoneConfig.value.trim() });
        carregarPerfilNoFormulario();
        Momentus.aplicarPerfilNaTela();
        const botao = formPerfil.querySelector('.botaoPrimario span');
        const original = botao.textContent;
        botao.textContent = Momentus.t('confAlteracoesSalvas');
        setTimeout(() => { botao.textContent = Momentus.t('confSalvarAlteracoes'); }, 2000);
    });

    document.addEventListener('momentus:idioma-alterado', () => {
        // Mantém o rótulo do botão sincronizado se não estiver em estado "salvo"
    });
}

const togglesPreferencia = {
    prefRsvp: 'rsvp',
    prefLembretes: 'lembretes',
    prefNovidades: 'novidades'
};
const algumToggle = Object.keys(togglesPreferencia).some((id) => document.getElementById(id));
if (algumToggle) {
    const prefs = Momentus.obterPreferencias();
    Object.entries(togglesPreferencia).forEach(([id, chave]) => {
        const el = document.getElementById(id);
        if (!el) return;
        el.checked = !!prefs[chave];
        el.addEventListener('change', () => {
            const atual = Momentus.obterPreferencias();
            atual[chave] = el.checked;
            Momentus.salvarPreferencias(atual);
        });
    });
}

/* ================= CONTADORES ANIMADOS (estatísticas) ================= */
function animarNumero(el) {
    const alvo = Number(el.dataset.count);
    const prefixo = el.dataset.prefix || '';
    const duracao = 900;
    const inicio = performance.now();
    const idioma = Momentus.obterIdioma();
    const locale = idioma === 'en' ? 'en-US' : idioma === 'es' ? 'es-ES' : 'pt-BR';

    function passo(agora) {
        const progresso = Math.min((agora - inicio) / duracao, 1);
        const facilitado = 1 - Math.pow(1 - progresso, 3);
        const valor = Math.round(alvo * facilitado);
        el.textContent = prefixo + valor.toLocaleString(locale);
        if (progresso < 1) requestAnimationFrame(passo);
    }
    requestAnimationFrame(passo);
}

const numerosStatEstaticos = document.querySelectorAll('.numeroStat[data-count]:not(#statEventos):not(#statConvidados):not(#statDias):not(#statOrcamento)');
if (numerosStatEstaticos.length) {
    const observador = new IntersectionObserver((entradas) => {
        entradas.forEach((entrada) => {
            if (entrada.isIntersecting) {
                animarNumero(entrada.target);
                observador.unobserve(entrada.target);
            }
        });
    }, { threshold: 0.4 });

    numerosStatEstaticos.forEach((el) => observador.observe(el));
}

/* ================= INCLINAÇÃO 3D SUAVE NOS CARDS ================= */
const cardsComInclinacao = document.querySelectorAll('.cardEvento, .cardProduto, .blocoCriarEvento, .corpoIngresso');

cardsComInclinacao.forEach((card) => {
    const alvo = card;

    card.addEventListener('mousemove', (e) => {
        const retangulo = alvo.getBoundingClientRect();
        const x = (e.clientX - retangulo.left) / retangulo.width - 0.5;
        const y = (e.clientY - retangulo.top) / retangulo.height - 0.5;
        const inclinacaoX = (y * -5).toFixed(2);
        const inclinacaoY = (x * 6).toFixed(2);
        alvo.style.transform = `perspective(60rem) rotateX(${inclinacaoX}deg) rotateY(${inclinacaoY}deg) translateY(-0.3rem)`;
    });

    card.addEventListener('mouseleave', () => {
        alvo.style.transform = '';
    });
});

/* ================= CAIXA DE NOTIFICAÇÕES (sino) ================= */
const botaoNotificacoes = document.getElementById('botaoNotificacoes');
if (botaoNotificacoes) {
    const painelNotificacoes = document.getElementById('painelNotificacoes');
    const corpoPainelNotificacoes = document.getElementById('corpoPainelNotificacoes');
    const bolinhaNotificacoes = document.getElementById('bolinhaNotificacoes');

    function renderizarPainelNotificacoes() {
        const notificacoes = Momentus.obterNotificacoes();
        bolinhaNotificacoes.classList.toggle('temNotificacao', notificacoes.some((n) => !n.lida));

        if (!notificacoes.length) {
            corpoPainelNotificacoes.innerHTML = `<div class="estadoVazioNotif">${Momentus.t('nenhumaNotificacao')}</div>`;
            return;
        }

        corpoPainelNotificacoes.innerHTML = notificacoes.map((n) => {
            if (n.tipo === 'convite-colaborador') {
                const texto = Momentus.t('notifConviteTexto', { evento: n.eventoNome || '' });
                let acoes = '';
                if (n.respondida) {
                    const tag = n.resposta === 'ativo' ? Momentus.t('notifAceitaTag') : Momentus.t('notifRecusadaTag');
                    acoes = `<span class="tagRespostaNotif">${escapeHTML(tag)}</span>`;
                } else {
                    acoes = `<div class="acoesNotificacao">
                        <button class="botaoAceitarNotif" data-acao="aceitar" data-notif="${n.id}" data-evento="${n.eventoId}" data-colab="${n.colaboradorId}">${Momentus.t('notifBotaoAceitar')}</button>
                        <button class="botaoRecusarNotif" data-acao="recusar" data-notif="${n.id}" data-evento="${n.eventoId}" data-colab="${n.colaboradorId}">${Momentus.t('notifBotaoRecusar')}</button>
                    </div>`;
                }
                return `<div class="itemNotificacao"><p>${escapeHTML(texto)}</p>${acoes}</div>`;
            }
            return '';
        }).join('');

        corpoPainelNotificacoes.querySelectorAll('[data-acao]').forEach((botao) => {
            botao.addEventListener('click', () => {
                const status = botao.dataset.acao === 'aceitar' ? 'ativo' : 'recusado';
                Momentus.responderColaborador(botao.dataset.evento, botao.dataset.colab, status);
                mostrarToast(status === 'ativo' ? Momentus.t('conviteAceitoToast') : Momentus.t('conviteRecusadoToast'));
                renderizarPainelNotificacoes();
            });
        });
    }

    function alternarPainelNotificacoes() {
        const abrindo = !painelNotificacoes.classList.contains('aberto');
        painelNotificacoes.classList.toggle('aberto', abrindo);
        if (abrindo) {
            renderizarPainelNotificacoes();
            Momentus.marcarNotificacoesLidas();
            bolinhaNotificacoes.classList.remove('temNotificacao');
        }
    }

    botaoNotificacoes.addEventListener('click', (e) => {
        e.stopPropagation();
        alternarPainelNotificacoes();
    });
    document.addEventListener('click', (e) => {
        if (painelNotificacoes.classList.contains('aberto') && !painelNotificacoes.contains(e.target) && e.target !== botaoNotificacoes) {
            painelNotificacoes.classList.remove('aberto');
        }
    });
    document.addEventListener('momentus:notificacoes-alteradas', () => {
        bolinhaNotificacoes.classList.toggle('temNotificacao', Momentus.obterNotificacoes().some((n) => !n.lida));
        if (painelNotificacoes.classList.contains('aberto')) renderizarPainelNotificacoes();
    });
    document.addEventListener('momentus:eventos-alterados', () => {
        if (painelNotificacoes.classList.contains('aberto')) renderizarPainelNotificacoes();
    });
    document.addEventListener('momentus:idioma-alterado', () => {
        if (painelNotificacoes.classList.contains('aberto')) renderizarPainelNotificacoes();
    });

    bolinhaNotificacoes.classList.toggle('temNotificacao', Momentus.obterNotificacoes().some((n) => !n.lida));
}
