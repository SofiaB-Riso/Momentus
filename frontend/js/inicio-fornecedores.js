(function () {
    const lista = document.getElementById('listaCatalogoInicio');
    if (!lista || typeof MomentusAPI === 'undefined' || typeof Momentus === 'undefined') return;

    const inputBusca = document.getElementById('filtroCatalogoInicio');
    const botaoLocalizacao = document.getElementById('botaoUsarLocalizacaoInicio');
    const inputCidade = document.getElementById('inputCidadeCatalogoInicio');
    const botaoBuscarCidade = document.getElementById('botaoBuscarCidadeInicio');
    const statusLocalizacao = document.getElementById('statusLocalizacaoInicio');

    const LIMITE_ITENS = 4;
    const escapeHTML = (v) => { const d = document.createElement('div'); d.textContent = String(v ?? ''); return d.innerHTML; };

    const estado = { termo: '', lat: null, lng: null, cidade: '' };
    let temporizadorBusca = null;

    function definirStatus(texto) {
        if (statusLocalizacao) statusLocalizacao.textContent = texto || '';
    }

    function estrelas(nota) {
        const n = Math.max(0, Math.min(5, Math.round(Number(nota) || 0)));
        return '★'.repeat(n) + '<span class="apagada">' + '★'.repeat(5 - n) + '</span>';
    }

    /* ---- Localização: reaproveitada do catálogo, automática ou cidade digitada ---- */
    function usarLocalizacaoSalva() {
        if (typeof MomentusLocalizacao === 'undefined') return false;
        const salva = MomentusLocalizacao.carregar();
        if (!salva) return false;
        estado.lat = salva.lat;
        estado.lng = salva.lng;
        estado.cidade = salva.cidade || '';
        if (inputCidade && salva.cidade) inputCidade.value = salva.cidade;
        definirStatus(salva.cidade ? `Perto de ${salva.cidade}.` : 'Usando sua localização atual.');
        carregar();
        return true;
    }

    function pedirLocalizacaoAutomatica() {
        if (usarLocalizacaoSalva()) return;
        if (!('geolocation' in navigator)) {
            definirStatus('Digite sua cidade para ver fornecedores.');
            return;
        }
        navigator.geolocation.getCurrentPosition(
            (posicao) => {
                estado.lat = posicao.coords.latitude;
                estado.lng = posicao.coords.longitude;
                estado.cidade = '';
                definirStatus('Usando sua localização atual.');
                if (typeof MomentusLocalizacao !== 'undefined') MomentusLocalizacao.salvar({ lat: estado.lat, lng: estado.lng, cidade: '' });
                carregar();
            },
            () => definirStatus('Toque em "Usar minha localização" ou digite sua cidade.'),
            { enableHighAccuracy: false, timeout: 8000 }
        );
    }

    if (botaoLocalizacao) {
        botaoLocalizacao.addEventListener('click', () => {
            if (!('geolocation' in navigator)) {
                definirStatus('Seu navegador não suporta localização automática — digite sua cidade.');
                return;
            }
            definirStatus('Pedindo permissão de localização...');
            navigator.geolocation.getCurrentPosition(
                (posicao) => {
                    estado.lat = posicao.coords.latitude;
                    estado.lng = posicao.coords.longitude;
                    estado.cidade = '';
                    if (inputCidade) inputCidade.value = '';
                    definirStatus('Usando sua localização atual.');
                    if (typeof MomentusLocalizacao !== 'undefined') MomentusLocalizacao.salvar({ lat: estado.lat, lng: estado.lng, cidade: '' });
                    carregar();
                },
                () => definirStatus('Não conseguimos acessar sua localização — digite sua cidade.'),
                { enableHighAccuracy: false, timeout: 8000 }
            );
        });
    }

    if (botaoBuscarCidade) {
        botaoBuscarCidade.addEventListener('click', () => {
            const cidade = (inputCidade.value || '').trim();
            if (!cidade) { definirStatus('Digite o nome de uma cidade.'); return; }
            estado.cidade = cidade;
            estado.lat = null;
            estado.lng = null;
            definirStatus(`Buscando fornecedores em ${cidade}...`);
            if (typeof MomentusLocalizacao !== 'undefined') MomentusLocalizacao.salvar({ lat: null, lng: null, cidade });
            carregar();
        });
    }
    if (inputCidade) {
        inputCidade.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') { e.preventDefault(); botaoBuscarCidade.click(); }
        });
    }

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
            lista.innerHTML = '<p class="estadoVazioClaro">Nenhum fornecedor encontrado por aqui.</p>';
            return;
        }
        lista.innerHTML = itens.slice(0, LIMITE_ITENS).map((f) => {
            const capaEstilo = f.foto_url
                ? `background-image:url('${f.foto_url.replace(/'/g, '%27')}');background-size:cover;background-position:center`
                : 'background:var(--grad-2)';
            return `<a class="itemCatalogo" href="catalogo.html?busca=${encodeURIComponent(f.nome_empresa)}">
                <div class="thumbCatalogo" style="${capaEstilo}"></div>
                <div class="infoCatalogo">
                    <div class="nomeCatalogo">${escapeHTML(f.nome_empresa)}</div>
                    <div class="descCatalogo">${escapeHTML(f.endereco || '')}</div>
                    <div class="estrelas">${estrelas(f.avaliacao)}</div>
                </div>
            </a>`;
        }).join('');
    }

    /* ---- Busca no backend (que fala com a Google Places API) ---- */
    async function carregar() {
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
            renderizar(resultados);
        } catch (e) {
            lista.innerHTML = `<p class="estadoVazioClaro">${escapeHTML(e.message)}</p>`;
        }
    }

    Momentus.aguardarEventosProntos().then(pedirLocalizacaoAutomatica);
})();
