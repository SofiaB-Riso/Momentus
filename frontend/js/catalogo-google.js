(function () {
    const grade = document.getElementById('grelhaCatalogo');
    if (!grade || typeof MomentusAPI === 'undefined' || typeof Momentus === 'undefined') return;

    const filtros = document.querySelectorAll('.filtroChip');
    const inputBusca = document.getElementById('buscaCatalogoGeral');
    const botaoLocalizacao = document.getElementById('botaoUsarLocalizacao');
    const inputCidade = document.getElementById('inputCidadeCatalogo');
    const botaoBuscarCidade = document.getElementById('botaoBuscarCidade');
    const statusLocalizacao = document.getElementById('statusLocalizacao');

    const escapeHTML = (v) => { const d = document.createElement('div'); d.textContent = String(v ?? ''); return d.innerHTML; };

    const estado = { termo: '', lat: null, lng: null, cidade: '', ultimosResultados: [] };
    let temporizadorBusca = null;

    function categoriaAtiva() {
        const ativo = document.querySelector('.filtroChip.ativoFiltro');
        return ativo ? ativo.dataset.filtro : 'todos';
    }

    function definirStatus(texto) {
        if (statusLocalizacao) statusLocalizacao.textContent = texto || '';
    }

    function chaveFornecedor(f) { return `google-${f.id}`; }

    function estrelas(nota) {
        const n = Math.max(0, Math.min(5, Math.round(Number(nota) || 0)));
        return '★'.repeat(n) + '<span class="apagada">' + '★'.repeat(5 - n) + '</span>';
    }

    /* ---- Localização: reaproveitada de outra página, automática (com permissão) ou cidade digitada ---- */
    function usarLocalizacaoSalva() {
        if (typeof MomentusLocalizacao === 'undefined') return false;
        const salva = MomentusLocalizacao.carregar();
        if (!salva) return false;
        estado.lat = salva.lat;
        estado.lng = salva.lng;
        estado.cidade = salva.cidade || '';
        if (inputCidade && salva.cidade) inputCidade.value = salva.cidade;
        definirStatus(salva.cidade ? `Usando fornecedores perto de ${salva.cidade}.` : 'Usando sua localização atual.');
        carregar();
        return true;
    }

    function forcarNovaLocalizacaoAutomatica() {
        if (!('geolocation' in navigator)) {
            definirStatus('Seu navegador não suporta localização automática — digite sua cidade abaixo.');
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
            () => definirStatus('Não conseguimos acessar sua localização — digite sua cidade abaixo.'),
            { enableHighAccuracy: false, timeout: 8000 }
        );
    }

    function pedirLocalizacaoAutomatica() {
        if (usarLocalizacaoSalva()) return;
        forcarNovaLocalizacaoAutomatica();
    }

    if (botaoLocalizacao) botaoLocalizacao.addEventListener('click', forcarNovaLocalizacaoAutomatica);

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

    /* ---- Filtros de categoria e busca por texto ---- */
    filtros.forEach((chip) => {
        chip.addEventListener('click', () => {
            filtros.forEach((f) => f.classList.remove('ativoFiltro'));
            chip.classList.add('ativoFiltro');
            if (chip.dataset.filtro === 'favoritos') {
                renderizar(estado.ultimosResultados.filter((f) => Momentus.ehFavorito(chaveFornecedor(f))));
            } else {
                carregar();
            }
        });
    });

    if (inputBusca) {
        inputBusca.addEventListener('input', () => {
            estado.termo = inputBusca.value.trim();
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
                    overlay.classList.remove('aberto');
                    if (typeof window.mostrarToast === 'function') window.mostrarToast('Item adicionado ao evento.');
                }
                b.disabled = false;
            }));
        }
        overlay.classList.add('aberto');
    }

    /* ---- Renderização dos cards ---- */
    function renderizar(lista) {
        if (!lista.length) {
            grade.innerHTML = '<p class="estadoVazioClaro"><strong>Nenhum fornecedor encontrado.</strong><br>Tente outra categoria, termo de busca ou cidade.</p>';
            return;
        }
        grade.innerHTML = lista.map((f) => {
            const chave = chaveFornecedor(f);
            const capaEstilo = f.foto_url
                ? `background-image:url('${f.foto_url.replace(/'/g, "%27")}');background-size:cover;background-position:center`
                : 'background:var(--grad-2)';
            return `<article class="cardProduto" data-chave="${chave}">
                <div class="capaProduto" style="${capaEstilo}">
                    <button class="tagFavorito" aria-label="Favoritar">${Momentus.ehFavorito(chave) ? '♥' : '♡'}</button>
                </div>
                <div class="corpoProduto">
                    <div class="nomeProduto">${escapeHTML(f.nome_empresa)}</div>
                    <div class="descProduto">${escapeHTML(f.endereco || '')}</div>
                    <div class="estrelas">${estrelas(f.avaliacao)} <span style="color:var(--tinta-suave)">(${f.total_avaliacoes || 0})</span></div>
                </div>
                <div class="rodapeProduto">
                    <span class="precoCatalogo">via Google</span>
                    <button class="botaoAdicionar" aria-label="Adicionar ao evento"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
                </div>
            </article>`;
        }).join('');

        grade.querySelectorAll('.cardProduto').forEach((card, i) => {
            const f = lista[i];
            const chave = card.dataset.chave;
            const fav = card.querySelector('.tagFavorito');
            fav.addEventListener('click', async () => {
                await Momentus.alternarFavorito(chave);
                fav.textContent = Momentus.ehFavorito(chave) ? '♥' : '♡';
            });
            card.querySelector('.botaoAdicionar').addEventListener('click', () => abrirEscolha(f));
        });
    }

    /* ---- Busca no backend, que por sua vez fala com a Google Places API ---- */
    async function carregar() {
        const categoria = categoriaAtiva();
        if (categoria === 'favoritos') {
            renderizar(estado.ultimosResultados.filter((f) => Momentus.ehFavorito(chaveFornecedor(f))));
            return;
        }
        const temLocalizacao = estado.cidade || (estado.lat !== null && estado.lng !== null);
        if (!temLocalizacao) {
            grade.innerHTML = '<p class="estadoVazioClaro">Toque em "Usar minha localização" ou digite sua cidade para ver fornecedores perto de você.</p>';
            return;
        }
        grade.innerHTML = '<p class="estadoVazioClaro">Buscando fornecedores...</p>';
        try {
            const resultados = await MomentusAPI.fornecedoresPerto({
                categoria,
                q: estado.termo,
                lat: estado.lat,
                lng: estado.lng,
                cidade: estado.cidade,
            });
            estado.ultimosResultados = resultados;
            renderizar(resultados);
        } catch (e) {
            grade.innerHTML = `<p class="estadoVazioClaro">${escapeHTML(e.message)}</p>`;
        }
    }

    /* ---- Se o usuário veio de outra página com um termo pronto (?busca=...), já preenche ---- */
    (function aplicarBuscaDaURL() {
        const parametros = new URLSearchParams(window.location.search);
        const termoURL = (parametros.get('busca') || '').trim();
        if (termoURL) {
            estado.termo = termoURL;
            if (inputBusca) inputBusca.value = termoURL;
        }
    })();

    Momentus.aguardarEventosProntos().then(pedirLocalizacaoAutomatica);
})();
