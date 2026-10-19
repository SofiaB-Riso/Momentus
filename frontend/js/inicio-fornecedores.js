(function () {
    const lista = document.getElementById('listaCatalogoInicio');
    if (!lista || typeof MomentusAPI === 'undefined' || typeof Momentus === 'undefined') return;

    const inputBusca = document.getElementById('filtroCatalogoInicio');
    const botaoLocalizacao = document.getElementById('botaoUsarLocalizacaoInicio');
    const inputCidade = document.getElementById('inputCidadeCatalogoInicio');
    const botaoBuscarCidade = document.getElementById('botaoBuscarCidadeInicio');
    const statusLocalizacao = document.getElementById('statusLocalizacaoInicio');

    const LIMITE_ITENS = 4;
    const { escapeHTML, estrelas } = MomentusUtils;

    const estado = { termo: '', lat: null, lng: null, cidade: '', precisao: null };
    let temporizadorBusca = null;
    let buscaAtual = 0;


    const iniciarLocalizacao = MomentusLocalizacao.conectar({
        estado, inputCidade, botaoLocalizacao, botaoBuscarCidade, statusLocalizacao,
        aoAlterar: carregar
    });

    if (inputBusca) {
        inputBusca.addEventListener('input', () => {
            estado.termo = inputBusca.value.trim();
            clearTimeout(temporizadorBusca);
            temporizadorBusca = setTimeout(carregar, 500);
        });
    }

    /* ---- Renderização compacta (sem botão de adicionar — leva para o catálogo completo) ---- */
    function renderizar(itens) {
        if (!itens.length) {
            lista.innerHTML = '<p class="estadoVazioClaro">Nenhum fornecedor encontrado nesta área. Tente outro termo ou busque por bairro e cidade.</p>';
            return;
        }
        lista.innerHTML = itens.slice(0, LIMITE_ITENS).map((f) => {
            return `<a class="itemCatalogo" href="catalogo.html?busca=${encodeURIComponent(f.nome_empresa)}">
                <div class="thumbCatalogo" style="background:var(--grad-2)"></div>
                <div class="infoCatalogo">
                    <div class="nomeCatalogo">${escapeHTML(f.nome_empresa)}</div>
                    <div class="descCatalogo">${escapeHTML(f.endereco || '')}</div>
                    <div class="distanciaFornecedor">${escapeHTML(MomentusLocalizacao.distancia(f.distancia_metros))}</div>
                    <div class="estrelas">${estrelas(f.avaliacao)}</div>
                </div>
            </a>`;
        }).join('');
    }

    /* ---- Busca no backend (que fala com a Google Places API) ---- */
    async function carregar() {
        const pedidoBusca = ++buscaAtual;
        const temLocalizacao = estado.cidade || (estado.lat !== null && estado.lng !== null);
        if (!temLocalizacao) {
            lista.innerHTML = '<p class="estadoVazioClaro">Toque em "Usar minha localização" para ver fornecedores perto de você.</p>';
            return;
        }
        lista.innerHTML = '<p class="estadoVazioClaro">Buscando fornecedores...</p>';
        try {
            const resultados = await MomentusAPI.fornecedoresPerto({
                categoria: 'todos',
                q: estado.termo,
                lat: estado.lat,
                lng: estado.lng,
                cidade: estado.cidade,
            });
            if (pedidoBusca !== buscaAtual) return;
            renderizar(resultados);
        } catch (e) {
            if (pedidoBusca !== buscaAtual) return;
            lista.innerHTML = `<p class="estadoVazioClaro">${escapeHTML(e.message)}</p>`;
        }
    }

    Momentus.aguardarEventosProntos().then(iniciarLocalizacao);
})();
