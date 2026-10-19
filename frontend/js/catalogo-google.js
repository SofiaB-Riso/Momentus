(function () {
    const grade = document.getElementById('grelhaCatalogo');
    if (!grade || typeof MomentusAPI === 'undefined' || typeof Momentus === 'undefined') return;

    const filtros = document.querySelectorAll('.filtroChip');
    const inputBusca = document.getElementById('buscaCatalogoGeral');
    const botaoLocalizacao = document.getElementById('botaoUsarLocalizacao');
    const inputCidade = document.getElementById('inputCidadeCatalogo');
    const botaoBuscarCidade = document.getElementById('botaoBuscarCidade');
    const statusLocalizacao = document.getElementById('statusLocalizacao');
    const botaoMais = document.getElementById('carregarMaisCatalogo');
    const statusPaginacao = document.getElementById('statusPaginacaoCatalogo');
    const criterioMelhores = document.getElementById('criterioMelhores');

    const { escapeHTML, estrelas } = MomentusUtils;

    const estado = { termo: '', lat: null, lng: null, cidade: '', precisao: null, ultimosResultados: [], proximaPagina: null, carregando: false, erro: '', pendentes: [], iniciouBusca: false, paginasVisitadas: new Set() };
    let temporizadorBusca = null;
    let buscaAtual = 0;

    const overlayEscolha = document.getElementById('overlayEscolherEvento');
    const botaoFecharEscolha = document.getElementById('fecharEscolherEvento');
    let focoAntesDaEscolha = null;

    function fecharEscolha() {
        if (!overlayEscolha) return;
        overlayEscolha.classList.remove('aberto');
        overlayEscolha.setAttribute('aria-hidden', 'true');
        overlayEscolha.inert = true;
        if (focoAntesDaEscolha?.isConnected) focoAntesDaEscolha.focus();
    }
    botaoFecharEscolha?.addEventListener('click', fecharEscolha);
    overlayEscolha?.addEventListener('click', (e) => {
        if (e.target === overlayEscolha) fecharEscolha();
    });
    document.addEventListener('keydown', (e) => {
        if (!overlayEscolha?.classList.contains('aberto')) return;
        if (e.key === 'Escape') { e.preventDefault(); fecharEscolha(); }
        if (e.key === 'Tab') {
            const botoes = [...overlayEscolha.querySelectorAll('button:not(:disabled)')];
            const primeiro = botoes[0], ultimo = botoes[botoes.length - 1];
            if (e.shiftKey && document.activeElement === primeiro) { e.preventDefault(); ultimo?.focus(); }
            else if (!e.shiftKey && document.activeElement === ultimo) { e.preventDefault(); primeiro?.focus(); }
        }
    });

    function categoriaAtiva() {
        const ativo = document.querySelector('.filtroChip.ativoFiltro');
        return ativo ? ativo.dataset.filtro : 'melhores';
    }

    function chaveFornecedor(f) { return `google-${f.id}`; }


    const iniciarLocalizacao = MomentusLocalizacao.conectar({
        estado, inputCidade, botaoLocalizacao, botaoBuscarCidade, statusLocalizacao,
        aoAlterar: carregar
    });

    /* ---- Filtros de categoria e busca por texto ---- */
    filtros.forEach((chip) => {
        chip.addEventListener('click', () => {
            filtros.forEach((f) => f.classList.remove('ativoFiltro'));
            chip.classList.add('ativoFiltro');
            clearTimeout(temporizadorBusca);
            carregar();
        });
    });

    if (inputBusca) {
        inputBusca.addEventListener('input', () => {
            estado.termo = inputBusca.value.trim();
            ++buscaAtual;
            estado.carregando = false;
            estado.proximaPagina = null;
            estado.pendentes = [];
            estado.iniciouBusca = false;
            estado.erro = '';
            atualizarPaginacao();
            clearTimeout(temporizadorBusca);
            temporizadorBusca = setTimeout(carregar, 500);
        });
    }

    /* ---- Modal "adicionar a um evento", igual ao usado no resto do catálogo ---- */
    function abrirEscolha(fornecedor) {
        const overlay = document.getElementById('overlayEscolherEvento');
        const corpo = document.getElementById('corpoEscolherEvento');
        const texto = document.getElementById('textoEscolherEvento');
        if (!overlay || !corpo) return;
        const eventos = Momentus.obterEventos();
        if (texto) texto.textContent = `Escolha em qual evento adicionar "${fornecedor.nome_empresa}".`;
        if (!eventos.length) {
            corpo.innerHTML = '<div class="estadoVazioClaro"><strong>Nenhum evento criado.</strong><br>Crie seu primeiro evento para usar o catálogo.</div>';
        } else {
            corpo.innerHTML = eventos.map((ev) => `<button class="opcaoEventoCatalogoBanco" data-evento="${ev.id}"><strong>${escapeHTML(ev.nome)}</strong><span>${escapeHTML(ev.data || '')}</span></button>`).join('');
            corpo.querySelectorAll('[data-evento]').forEach((b) => b.addEventListener('click', async () => {
                b.disabled = true;
                const item = await Momentus.adicionarItemCatalogo(b.dataset.evento, {
                    produtoId: fornecedor.id,
                    nome: fornecedor.nome_empresa,
                    categoria: fornecedor.categoria,
                    preco: 0,
                });
                if (item) {
                    fecharEscolha();
                    if (typeof window.mostrarToast === 'function') window.mostrarToast('Item adicionado ao evento.');
                }
                b.disabled = false;
            }));
        }
        focoAntesDaEscolha = document.activeElement;
        overlay.inert = false;
        overlay.setAttribute('aria-hidden', 'false');
        overlay.classList.add('aberto');
        botaoFecharEscolha?.focus();
    }

    /* ---- Renderização dos cards ---- */
    function renderizar(lista) {
        if (!lista.length) {
            const texto = categoriaAtiva() === 'melhores' ? Momentus.t('catalogoSemMelhores') : Momentus.t('catalogoSemResultados');
            grade.innerHTML = `<p class="estadoVazioClaro">${escapeHTML(texto)}${estado.proximaPagina ? '<br>' + escapeHTML(Momentus.t('catalogoProximaDisponivel')) : ''}</p>`;
            return;
        }
        grade.innerHTML = lista.map((f) => {
            const chave = chaveFornecedor(f);
            return `<article class="cardProduto" data-chave="${escapeHTML(chave)}">
                <div class="capaProduto" style="background:var(--grad-2)">
                    <button class="tagFavorito" aria-label="Favoritar">${Momentus.ehFavorito(chave) ? '♥' : '♡'}</button>
                </div>
                <div class="linksEstabelecimento"></div>
                <div class="corpoProduto">
                    <div class="nomeProduto">${escapeHTML(f.nome_empresa)}</div>
                    <div class="descProduto">${escapeHTML(f.endereco || '')}</div>
                    <div class="distanciaFornecedor">${escapeHTML(MomentusLocalizacao.distancia(f.distancia_metros))}</div>
                    <div class="estrelas">${estrelas(f.avaliacao)} <span class="notaCatalogo">${escapeHTML(f.avaliacao == null ? '—' : Number(f.avaliacao).toLocaleString(undefined, { maximumFractionDigits: 1 }))}</span> <span style="color:var(--tinta-suave)">(${f.total_avaliacoes || 0})</span></div>
                </div>
                <div class="rodapeProduto">
                    <span class="precoCatalogo">via Google</span>
                    <button class="botaoAdicionar" aria-label="Adicionar ao evento"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
                </div>
            </article>`;
        }).join('');

        grade.querySelectorAll('.cardProduto').forEach((card, i) => {
            const f = lista[i];
            prepararLinks(card, f);
            const chave = card.dataset.chave;
            const fav = card.querySelector('.tagFavorito');
            fav.addEventListener('click', async () => {
                await Momentus.alternarFavorito(chave);
                fav.textContent = Momentus.ehFavorito(chave) ? '♥' : '♡';
            });
            card.querySelector('.botaoAdicionar').addEventListener('click', () => abrirEscolha(f));
        });
    }

    function urlSegura(valor) {
        if (!valor) return '';
        try {
            const url = new URL(valor, location.origin);
            return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
        } catch { return ''; }
    }

    function prepararLinks(card, fornecedor) {
        const links = card.querySelector('.linksEstabelecimento');
        for (const [url, texto] of [
            [fornecedor.google_maps_url, 'Google Maps'],
            [fornecedor.street_view_url, Momentus.t('verStreetView')],
        ]) {
            const href = urlSegura(url);
            if (!href) continue;
            const link = document.createElement('a');
            link.href = href;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.textContent = texto;
            links.appendChild(link);
        }
    }

    const TAMANHO_LOTE = 20;

    function temMaisResultados() {
        return estado.pendentes.length > 0 || Boolean(estado.proximaPagina)
            || Boolean(estado.erro && !estado.iniciouBusca);
    }

    function atualizarPaginacao() {
        const favoritos = categoriaAtiva() === 'favoritos';
        criterioMelhores.hidden = categoriaAtiva() !== 'melhores';
        botaoMais.hidden = favoritos || !temMaisResultados();
        botaoMais.disabled = estado.carregando;
        botaoMais.textContent = Momentus.t(estado.carregando ? 'carregandoCatalogo' : 'carregarMaisCatalogo');
        grade.setAttribute('aria-busy', String(estado.carregando));
        if (favoritos || estado.carregando) { statusPaginacao.textContent = ''; return; }
        if (estado.erro) { statusPaginacao.textContent = estado.erro; return; }
        const total = estado.ultimosResultados.length;
        statusPaginacao.textContent = total
            ? Momentus.t('catalogoContagem', { quantidade: total }) + (temMaisResultados() ? '' : ' ' + Momentus.t('catalogoFim'))
            : (temMaisResultados() ? Momentus.t('catalogoProximaDisponivel') : '');
    }

    function ordenarResultados(lista, categoria) {
        return lista.sort((a, b) => {
            if (categoria === 'melhores') {
                const qualidade = (b.avaliacao - a.avaliacao) || (b.total_avaliacoes - a.total_avaliacoes);
                if (qualidade) return qualidade;
            }
            return (a.distancia_metros ?? Infinity) - (b.distancia_metros ?? Infinity);
        });
    }

    /* Completa lotes de 20 únicos, buscando mais páginas somente quando faltar completar o lote. */
    async function carregar(mais = false) {
        if (mais && (estado.carregando || !temMaisResultados())) return;
        const pedidoBusca = ++buscaAtual;
        const categoria = categoriaAtiva();
        estado.carregando = false;
        estado.erro = '';
        if (categoria === 'favoritos') {
            renderizar(estado.ultimosResultados.filter((f) => Momentus.ehFavorito(chaveFornecedor(f))));
            atualizarPaginacao();
            return;
        }
        if (!mais) {
            estado.proximaPagina = null;
            estado.ultimosResultados = [];
            estado.pendentes = [];
            estado.iniciouBusca = false;
            estado.paginasVisitadas = new Set();
        }
        const temLocalizacao = estado.cidade || (estado.lat !== null && estado.lng !== null);
        if (!temLocalizacao) {
            grade.innerHTML = '<p class="estadoVazioClaro">Toque em "Usar minha localização" ou digite seu bairro e cidade para ver fornecedores perto de você.</p>';
            atualizarPaginacao();
            return;
        }
        estado.carregando = true;
        atualizarPaginacao();
        if (!mais) grade.innerHTML = '<p class="estadoVazioClaro">Buscando fornecedores...</p>';
        try {
            const visiveis = new Set(estado.ultimosResultados.map(f => f.id));
            const candidatos = new Map(estado.pendentes.map(f => [f.id, f]));
            while (candidatos.size < TAMANHO_LOTE && (!estado.iniciouBusca || estado.proximaPagina)) {
                const paginaSolicitada = estado.iniciouBusca ? estado.proximaPagina : null;
                const resultado = await MomentusAPI.fornecedoresPerto({
                    categoria, q: estado.termo, lat: estado.lat, lng: estado.lng,
                    cidade: estado.cidade, paginado: 1, pagina: paginaSolicitada,
                });
                if (pedidoBusca !== buscaAtual) return;
                for (const fornecedor of resultado.fornecedores) {
                    if (!visiveis.has(fornecedor.id)) candidatos.set(fornecedor.id, fornecedor);
                }
                // Preserva o que já foi recebido se uma página seguinte falhar.
                estado.pendentes = [...candidatos.values()];
                estado.iniciouBusca = true;
                estado.paginasVisitadas.add(paginaSolicitada);
                const proxima = resultado.proxima_pagina;
                estado.proximaPagina = proxima && !estado.paginasVisitadas.has(proxima) ? proxima : null;
            }
            const ordenados = ordenarResultados([...candidatos.values()], categoria);
            const novos = ordenados.slice(0, TAMANHO_LOTE);
            estado.pendentes = ordenados.slice(TAMANHO_LOTE);
            estado.ultimosResultados = ordenarResultados([...estado.ultimosResultados, ...novos], categoria);
            renderizar(estado.ultimosResultados);
        } catch (e) {
            if (pedidoBusca !== buscaAtual) return;
            estado.erro = e.message;
            if (!mais) grade.innerHTML = `<p class="estadoVazioClaro">${escapeHTML(e.message)}</p>`;
        } finally {
            if (pedidoBusca === buscaAtual) {
                estado.carregando = false;
                atualizarPaginacao();
            }
        }
    }

    botaoMais.addEventListener('click', () => carregar(true));

    /* ---- Se o usuário veio de outra página com um termo pronto (?busca=...), já preenche ---- */
    (function aplicarBuscaDaURL() {
        const parametros = new URLSearchParams(window.location.search);
        const termoURL = (parametros.get('busca') || '').trim();
        if (termoURL) {
            estado.termo = termoURL;
            if (inputBusca) inputBusca.value = termoURL;
        }
    })();

    document.addEventListener('momentus:idioma-alterado', () => {
        renderizar(categoriaAtiva() === 'favoritos' ? estado.ultimosResultados.filter((f) => Momentus.ehFavorito(chaveFornecedor(f))) : estado.ultimosResultados);
        atualizarPaginacao();
    });
    atualizarPaginacao();
    Momentus.aguardarEventosProntos().then(iniciarLocalizacao);
})();
