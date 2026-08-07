/* ================= TODOS OS EVENTOS ================= */
(function () {
    const grelha = document.getElementById('grelhaEventos');
    if (!grelha) return;

    const busca = document.getElementById('buscaEventos');
    let termoBusca = '';

    function corGrupo(indice) {
        return ['var(--grad-1)', 'var(--grad-2)', 'var(--grad-3)'][indice % 3];
    }

    function renderizar() {
        let eventos = Momentus.obterEventos().slice().sort((a, b) => (a.data + a.hora).localeCompare(b.data + b.hora));

        if (termoBusca) {
            const termo = termoBusca.toLowerCase();
            eventos = eventos.filter((ev) =>
                (ev.nome || '').toLowerCase().includes(termo) ||
                (ev.local || '').toLowerCase().includes(termo) ||
                (ev.tipoLabel || '').toLowerCase().includes(termo)
            );
        }

        if (!eventos.length) {
            grelha.innerHTML = `
                <div class="estadoVazioGeral">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 2 4 7v10l8 5 8-5V7l-8-5Z"/><path d="M4 7l8 5 8-5"/><path d="M12 22V12"/></svg>
                    <strong>${Momentus.t('nenhumEventoCriadoTitulo')}</strong>
                    <p>${Momentus.t('nenhumEventoCriadoTexto')}</p>
                    <a href="planejar.html" class="botaoPrimario">${Momentus.t('planejarEvento')}</a>
                </div>`;
            return;
        }

        grelha.innerHTML = eventos.map((ev, i) => {
            const statusChave = STATUS_LABEL_CHAVE[ev.status] || 'statusAgendado';
            const emoji = TIPO_EMOJI[ev.tipo] || '✨';
            return `
            <div class="cardEventoResumo" data-id="${ev.id}">
                <div class="capaEventoResumo abrirEvento" style="background:${corGrupo(i)}">
                    <div class="cabecalhoCard">
                        <span class="emojiTipo">${emoji}</span>
                        <span class="statusPill">${Momentus.t(statusChave)}</span>
                    </div>
                    <div class="nomeEventoResumo">${escapeHTML(ev.nome || ev.tipoLabel)}</div>
                </div>
                <div class="corpoEventoResumo abrirEvento">
                    <div class="linhaInfoResumo">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                        ${formatarDataBR(ev.data)}${ev.hora && ev.hora !== '—' ? ' · ' + escapeHTML(ev.hora) : ''}
                    </div>
                    <div class="linhaInfoResumo">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                        ${escapeHTML(ev.local || '—')}
                    </div>
                    <div class="linhaInfoResumo">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                        ${(ev.convidados || 0)} ${Momentus.t('cardEventoConvidados')}
                    </div>
                </div>
                <div class="rodapeEventoResumo">
                    <button class="botaoResumoAcao editarAcao" data-editar="${ev.id}">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
                        ${Momentus.t('botaoEditar')}
                    </button>
                    <button class="botaoResumoAcao apagarAcao" data-apagar="${ev.id}">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/></svg>
                        ${Momentus.t('botaoApagar')}
                    </button>
                </div>
            </div>`;
        }).join('');

        grelha.querySelectorAll('.abrirEvento').forEach((el) => {
            el.addEventListener('click', () => {
                const id = el.closest('.cardEventoResumo').dataset.id;
                window.location.href = 'evento.html?id=' + encodeURIComponent(id);
            });
        });

        grelha.querySelectorAll('[data-editar]').forEach((btn) => {
            btn.addEventListener('click', () => {
                window.location.href = 'planejar.html?id=' + encodeURIComponent(btn.dataset.editar);
            });
        });

        grelha.querySelectorAll('[data-apagar]').forEach((btn) => {
            btn.addEventListener('click', async () => {
                const ev = Momentus.obterEvento(btn.dataset.apagar);
                const nome = ev ? (ev.nome || ev.tipoLabel) : '';
                if (window.confirm(Momentus.t('confirmarApagarEvento', { nome }))) {
                    await Momentus.removerEvento(btn.dataset.apagar);
                }
            });
        });
    }

    if (busca) {
        busca.addEventListener('input', (e) => {
            termoBusca = e.target.value;
            renderizar();
        });
    }

    // Espera a primeira sincronização com o backend antes de desenhar a
    // tela pela primeira vez (evita mostrar "nenhum evento" por engano
    // enquanto a API ainda está respondendo).
    Momentus.aguardarEventosProntos().then(renderizar);
    document.addEventListener('momentus:eventos-alterados', renderizar);
    document.addEventListener('momentus:idioma-alterado', renderizar);
})();
