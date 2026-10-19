/* Preferências de busca compartilhadas entre Início e Catálogo. */
const MomentusLocalizacao = (() => {
    const CHAVE = 'momentus_localizacao_fornecedores';
    const opcoes = { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 };
    function salvar({ lat = null, lng = null, cidade = '', precisao = null }) {
        try { localStorage.setItem(CHAVE, JSON.stringify({ lat, lng, cidade, precisao, quando: Date.now(), versao: 2 })); } catch (_) {}
    }
    function carregar() {
        try {
            const dados = JSON.parse(localStorage.getItem(CHAVE));
            if (!dados || dados.versao !== 2 || !Number.isFinite(dados.quando)) return null;
            const idade = Date.now() - dados.quando;
            if (idade < 0 || idade > (dados.cidade ? 6 * 3600000 : 10 * 60000)) return null;
            if (dados.cidade) return { ...dados, lat: null, lng: null };
            if (!Number.isFinite(dados.lat) || !Number.isFinite(dados.lng) || Math.abs(dados.lat) > 90 || Math.abs(dados.lng) > 180) return null;
            return dados;
        } catch (_) { return null; }
    }
    function limpar() { try { localStorage.removeItem(CHAVE); } catch (_) {} }
    function status(dados, salva = false) {
        if (dados.cidade) return `Busca por bairro/cidade: ${dados.cidade}.`;
        const precisao = Number.isFinite(dados.precisao) ? Math.ceil(dados.precisao) : null;
        return `${salva ? 'Usando localização salva recentemente.' : 'Usando a localização do navegador.'} Mais próximos primeiro.`
            + (precisao !== null ? ` Precisão aproximada: ±${precisao} m.` : '')
            + (precisao > 1000 ? ' Para buscar no seu bairro, digite bairro e cidade.' : '');
    }
    function distancia(metros) {
        if (!Number.isFinite(metros) || metros < 0) return '';
        const valor = metros < 1000 ? `${Math.round(metros)} m` : `${(metros / 1000).toLocaleString('pt-BR', { maximumFractionDigits: 1 })} km`;
        return `${valor} em linha reta`;
    }
    /* Cada página fornece seus controles e recebe a mesma regra de localização. */
    function conectar({ estado, inputCidade, botaoLocalizacao, botaoBuscarCidade, statusLocalizacao, aoAlterar }) {
        let pedidoAtual = 0;
        const definirStatus = texto => { if (statusLocalizacao) statusLocalizacao.textContent = texto; };

        function aplicar(dados, salva = false) {
            Object.assign(estado, {
                lat: dados.lat ?? null, lng: dados.lng ?? null,
                cidade: dados.cidade || '', precisao: dados.precisao ?? null
            });
            if (inputCidade) inputCidade.value = estado.cidade;
            definirStatus(status(estado, salva));
            if (!salva) salvar(estado);
            aoAlterar();
        }

        function pedirLocalizacao() {
            if (!('geolocation' in navigator)) {
                definirStatus('Seu navegador não suporta localização automática — digite seu bairro e cidade.');
                return;
            }
            definirStatus('Pedindo permissão de localização...');
            const pedido = ++pedidoAtual;
            navigator.geolocation.getCurrentPosition(
                posicao => {
                    if (pedido !== pedidoAtual) return;
                    aplicar({ lat: posicao.coords.latitude, lng: posicao.coords.longitude, precisao: posicao.coords.accuracy });
                },
                () => {
                    if (pedido === pedidoAtual) definirStatus('Não conseguimos acessar sua localização — digite seu bairro e cidade.');
                },
                opcoes
            );
        }

        botaoLocalizacao?.addEventListener('click', pedirLocalizacao);
        botaoBuscarCidade?.addEventListener('click', () => {
            const cidade = (inputCidade?.value || '').trim();
            if (!cidade) { definirStatus('Digite o bairro e a cidade, ou só a cidade.'); return; }
            ++pedidoAtual; // Uma resposta atrasada do GPS não substitui a cidade digitada.
            aplicar({ cidade });
        });
        inputCidade?.addEventListener('keydown', evento => {
            if (evento.key === 'Enter') { evento.preventDefault(); botaoBuscarCidade?.click(); }
        });

        return function iniciar() {
            const salva = carregar();
            if (salva) aplicar(salva, true);
            else pedirLocalizacao();
        };
    }

    return { salvar, carregar, limpar, status, distancia, opcoes, conectar };
})();
