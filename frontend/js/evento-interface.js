/* Apresentação do evento: navegação, indicadores e ícones sem novas chamadas à API. */
window.MomentusEventoUI = (() => {
    const desenhos = {
        visao: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
        pessoas: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
        colaboracao: '<path d="m8 12 3 3 5-5M8 4H5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-3"/><rect x="8" y="2" width="8" height="4" rx="1"/>',
        tarefas: '<path d="m3 6 2 2 4-4M12 6h9M3 13l2 2 4-4M12 13h9M5 20h.01M12 20h9"/>',
        itens: '<path d="m12 3 9 5-9 5-9-5 9-5ZM3 8v9l9 5 9-5V8M12 13v9M7.5 5.5l9 5"/>',
        local: '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
        carteira: '<path d="M20 7V5a2 2 0 0 0-2-2H5a3 3 0 0 0 0 6h15v12H5a3 3 0 0 1-3-3V6M20 12h-5v5h5"/><path d="M16.5 14.5h.01"/>',
        despesa: '<path d="M5 3h14v19l-3-2-4 2-4-2-3 2V3ZM9 7h6M9 11h6M9 15h3"/>',
        propostas: '<path d="M8 3H3v18h5M16 3h5v18h-5M8 7h3M8 12h3M8 17h3M14 5v14M17 7h1M17 12h1M17 17h1"/>',
        galeria: '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="1.5"/><path d="m21 15-6-6-9 12"/>',
        historico: '<path d="M3 11a9 9 0 1 1 2.5 7M3 4v7h7M12 7v5l3 2"/>',
        calendario: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18M8 15h2M14 15h2"/>',
        editar: '<path d="m16 3 5 5-12 12-6 1 1-6L16 3ZM14 5l5 5"/>',
        lixeira: '<path d="M3 6h18M9 6V3h6v3M5 6l1 15h12l1-15M10 10v7M14 10v7"/>',
        ampulheta: '<path d="M5 3h14M5 21h14M7 3v4l10 10v4M17 3v4L7 17v4M7 7l10 10M17 7 7 17"/>'
    };
    let ativarAtual = null;
    function icone(nome) {
        return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (desenhos[nome] || desenhos.visao) + '</svg>';
    }
    window.addEventListener('hashchange', () => ativarAtual?.(location.hash.slice(1)));

    function ligar(evento, container, abaInicial) {
        const $ = id => container.querySelector('#' + id);
        container.querySelectorAll('[data-icone-evento]').forEach(el => { el.innerHTML = icone(el.dataset.iconeEvento); });
        const tipos = {aniversario:'catAniversario', casamento:'catCasamento', churrasco:'catChurrasco', formatura:'catFormatura', corporativo:'catCorporativo', noivado:'catNoivado', batizado:'catBatizado', confraternizacao:'catConfraternizacao'};
        const tipo = String(evento.tipo || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
        if (tipos[tipo]) $('tagTipoEvento').textContent = Momentus.t(tipos[tipo]);
        const pessoas = evento.listaConvidados || [];
        const tarefas = evento.tarefas || [];
        const feitas = tarefas.filter(t => t.feita).length;
        // O anel acompanha o checklist, inclusive em registros antigos que
        // guardavam uma porcentagem inicial sem tarefas concluídas.
        const progresso = tarefas.length ? Math.round(100 * feitas / tarefas.length) : 0;
        $('progressoTexto').textContent = progresso + '%';
        $('progressoBarra').style.setProperty('--progresso', progresso + '%');
        $('progressoBarra').setAttribute('aria-valuenow', String(progresso));
        $('resumoConfirmadosEvento').textContent = pessoas.filter(p => p.status === 'confirmado').length;
        $('resumoConvidadosEvento').textContent = pessoas.length ? 'de ' + pessoas.length + ' pessoa(s) convidada(s)' : 'Nenhum convite ainda';
        $('resumoTarefasEvento').textContent = feitas + ' de ' + tarefas.length;
        $('resumoProgressoEvento').textContent = tarefas.length ? feitas + ' de ' + tarefas.length + ' tarefas concluídas' : 'Comece pelo seu checklist.';
        $('resumoOrcamentoEvento').textContent = evento.orcamento ? formatarMoeda(evento.orcamento) : 'A definir';
        $('resumoDespesasEvento').textContent = formatarMoeda(evento.totalDespesas || 0);
        const data = new Date(evento.data + 'T00:00:00');
        const hoje = new Date();
        if (Number.isFinite(data.getTime())) {
            const dias = Math.round((Date.UTC(data.getFullYear(), data.getMonth(), data.getDate()) - Date.UTC(hoje.getFullYear(), hoje.getMonth(), hoje.getDate())) / 86400000);
            $('contagemMomentoEvento').textContent = dias > 1 ? `Faltam ${dias} dias` : dias === 1 ? 'É amanhã!' : dias === 0 ? 'O grande dia é hoje!' : 'Um dia na sua história';
            $('diaDestaqueEvento').textContent = String(data.getDate()).padStart(2, '0');
            $('mesDestaqueEvento').textContent = data.toLocaleDateString('pt-BR', {month:'short'}).replace('.', '');
            $('dataDestaqueEvento').textContent = data.toLocaleDateString('pt-BR', {day:'numeric', month:'long', year:'numeric'}) + (evento.hora && evento.hora !== '—' ? ' · ' + evento.hora : '');
        }
        const pendentes = tarefas.filter(t => !t.feita).slice().sort((a,b) => (a.prazo || '9999').localeCompare(b.prazo || '9999'));
        const proxima = pendentes[0];
        $('proximoPassoTitulo').textContent = proxima ? proxima.titulo
            : tarefas.length ? 'Tudo em dia por aqui' : 'Comece pelo primeiro passo';
        $('proximoPassoPrazo').textContent = proxima?.prazo
            ? 'Prazo: ' + new Date(proxima.prazo).toLocaleString('pt-BR', {day:'2-digit', month:'short', hour:'2-digit', minute:'2-digit'})
            : proxima ? 'Uma tarefa de cada vez aproxima o seu momento.'
            : tarefas.length ? 'Todos os itens do seu checklist estão concluídos.' : 'Adicione as tarefas que vão dar forma ao seu evento.';
        const acesso = document.getElementById('acessoEventoTexto');
        acesso.textContent = evento.permissao === 'dono' ? 'Seu evento' : evento.podeEditar === false ? 'Somente leitura' : 'Planejamento compartilhado';
        acesso.dataset.acesso = evento.podeEditar === false ? 'leitura' : 'edicao';

        const camposInfo = ['local', 'calendario', 'pessoas', 'visao', 'carteira', 'despesa'];
        container.querySelectorAll('.blocoInfoEvento').forEach((el, i) => {
            const marca = document.createElement('span');
            marca.className = 'iconeBlocoInfoEvento'; marca.setAttribute('aria-hidden', 'true');
            marca.innerHTML = icone(camposInfo[i]); el.prepend(marca);
        });
        const contagens = {
            convidados: pessoas.length,
            colaboracao: (evento.colaboradores || []).length,
            tarefas: tarefas.length - feitas,
            itens: (evento.itensCatalogo || []).length,
            financeiro: (evento.despesas || []).length,
            galeria: (evento.fotos || []).length
        };
        container.querySelectorAll('[data-contador-aba]').forEach(el => {
            const n = contagens[el.dataset.contadorAba] || 0;
            el.textContent = n; el.hidden = !n;
            if (el.dataset.contadorAba === 'tarefas') el.title = n + ' tarefa(s) pendente(s)';
        });

        const seletor = $('seletorAbaEvento');
        const abas = [...container.querySelectorAll('.abaEvento')];
        const paineis = [...container.querySelectorAll('.painelAba')];
        const historico = abas.find(a => a.dataset.aba === 'historico');
        if (evento.permissao !== 'dono') {
            historico.hidden = true;
            seletor.querySelector('[value="historico"]').remove();
        }
        const disponiveis = abas.filter(a => !a.hidden);
        function ativar(nome, registrar = false) {
            const escolhida = disponiveis.find(a => a.dataset.aba === nome) || disponiveis[0];
            const mudou = !escolhida.classList.contains('abaAtiva');
            abas.forEach(a => {
                const ativa = a === escolhida;
                a.classList.toggle('abaAtiva', ativa);
                a.setAttribute('aria-selected', String(ativa)); a.tabIndex = ativa ? 0 : -1;
            });
            paineis.forEach(p => {
                const ativa = p.dataset.painel === escolhida.dataset.aba;
                p.id = 'painelEvento-' + p.dataset.painel; p.setAttribute('role', 'tabpanel');
                p.setAttribute('aria-labelledby', 'abaEvento-' + p.dataset.painel); p.tabIndex = 0;
                p.classList.toggle('ativoPainel', ativa); p.hidden = !ativa;
                if (ativa && mudou && registrar && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
                    p.animate([{opacity:.6, transform:'translateY(5px)'},{opacity:1, transform:'translateY(0)'}], {duration:180, easing:'ease-out'});
                }
            });
            seletor.value = escolhida.dataset.aba;
            $('iconeSecaoEvento').innerHTML = icone(escolhida.querySelector('[data-icone-evento]').dataset.iconeEvento);
            if (registrar) {
                const url = new URL(location.href); url.hash = escolhida.dataset.aba;
                history.replaceState(null, '', url);
                const painel = paineis.find(p => !p.hidden);
                const limite = painel.getBoundingClientRect();
                if (limite.top < 0 || limite.top > innerHeight - 96) {
                    painel.scrollIntoView({block:'start', behavior:matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
                }
            }
        }
        abas.forEach(a => {
            a.addEventListener('click', () => ativar(a.dataset.aba, true));
            a.addEventListener('keydown', e => {
                if (!['ArrowDown','ArrowUp','Home','End'].includes(e.key)) return;
                e.preventDefault(); let i = disponiveis.indexOf(a);
                if (e.key === 'Home') i = 0;
                else if (e.key === 'End') i = disponiveis.length - 1;
                else i = (i + (e.key === 'ArrowDown' ? 1 : -1) + disponiveis.length) % disponiveis.length;
                ativar(disponiveis[i].dataset.aba, true); disponiveis[i].focus();
            });
        });
        seletor.addEventListener('change', () => ativar(seletor.value, true));
        container.querySelectorAll('[data-abrir-aba]').forEach(botao => botao.addEventListener('click', () => ativar(botao.dataset.abrirAba, true)));
        ativarAtual = nome => { if (container.isConnected && container.querySelector('#seletorAbaEvento')) ativar(nome); };
        ativar(abaInicial || location.hash.slice(1));
    }
    return { ligar };
})();
