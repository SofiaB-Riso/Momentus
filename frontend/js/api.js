const API_BASE_URL = '';

const MomentusAPI = (() => {
    let csrf = null;
    async function obterCsrf() {
        if (!csrf) csrf = fetch('/auth/csrf', {credentials:'same-origin',cache:'no-store'})
            .then(async resposta => {if (!resposta.ok) throw new Error('Não foi possível preparar o envio. Recarregue a página.');return (await resposta.json()).token;})
            .catch(erro => {csrf=null;throw erro;});
        return csrf;
    }
    async function requisitar(caminho, opcoes = {}, repeticaoCsrf = false) {
        const headers = Object.assign({}, opcoes.headers || {});
        const temBodyJSON = opcoes.body && !(opcoes.body instanceof FormData);
        if (temBodyJSON && !headers['Content-Type']) headers['Content-Type'] = 'application/json';
        const mutacao = !['GET','HEAD','OPTIONS'].includes((opcoes.method || 'GET').toUpperCase());
        if (mutacao) headers['X-CSRF-Token'] = await obterCsrf();

        let resposta;
        try {
            resposta = await fetch(API_BASE_URL + caminho, Object.assign({
                credentials: 'same-origin',
            }, opcoes, {headers}));
        } catch (erroDeRede) {
            const erro = new Error('Não foi possível conectar ao Momentus. Abra o site pelo Flask em http://127.0.0.1:5000.');
            erro.semConexao = true;
            throw erro;
        }

        if (['/auth/login','/auth/cadastro','/auth/logout','/auth/redefinir-senha','/auth/conta'].includes(caminho) && resposta.ok) csrf = null;
        if (resposta.status === 204) return null;

        const tipo = resposta.headers.get('content-type') || '';
        let corpo = null;
        if (tipo.includes('application/json')) {
            try { corpo = await resposta.json(); } catch (_) { corpo = null; }
        } else {
            corpo = await resposta.text();
        }

        if (!resposta.ok) {
            if (corpo?.codigo === 'CSRF_INVALID' && !repeticaoCsrf) {
                csrf = null;
                return requisitar(caminho, opcoes, true);
            }
            if (corpo?.codigo === 'AUTHORIZATION_REQUIRED' && !location.pathname.endsWith('configuracoes.html')) {
                location.href = 'configuracoes.html#autorizacaoContaConfig';
            }
            const mensagem = corpo && corpo.erro ? corpo.erro : 'Ocorreu um erro ao falar com o servidor.';
            const erro = new Error(mensagem);
            erro.status = resposta.status;
            erro.corpo = corpo;
            throw erro;
        }
        return corpo;
    }

    return {
        requisitar,
        me: () => requisitar('/auth/me'),
        login: (payload) => requisitar('/auth/login', { method: 'POST', body: JSON.stringify(payload) }),
        cadastro: (payload) => requisitar('/auth/cadastro', { method: 'POST', body: JSON.stringify(payload) }),
        logout: () => requisitar('/auth/logout', { method: 'POST' }),
        atualizarPerfil: (payload) => requisitar('/auth/perfil', { method: 'PUT', body: JSON.stringify(payload) }),
        excluirConta: () => requisitar('/auth/conta', { method: 'DELETE' }),

        listarEventos: () => requisitar('/eventos'),
        buscarEvento: (id) => requisitar('/eventos/' + encodeURIComponent(id)),
        buscarPorTipo: (tipo) => requisitar('/eventos/por-tipo?tipo_evento=' + encodeURIComponent(tipo)),
        criarEvento: (payload) => requisitar('/eventos', { method: 'POST', body: JSON.stringify(payload) }),
        atualizarEvento: (id, payload) => requisitar('/eventos/' + encodeURIComponent(id), { method: 'PUT', body: JSON.stringify(payload) }),
        removerEvento: (id) => requisitar('/eventos/' + encodeURIComponent(id), { method: 'DELETE' }),

        adicionarConvidado: (eventoId, payload) => requisitar(`/eventos/${eventoId}/convidados`, { method: 'POST', body: JSON.stringify(payload) }),
        atualizarConvidado: (eventoId, convidadoId, payload) => requisitar(`/eventos/${eventoId}/convidados/${convidadoId}`, { method: 'PUT', body: JSON.stringify(payload) }),
        removerConvidado: (eventoId, convidadoId) => requisitar(`/eventos/${eventoId}/convidados/${convidadoId}`, { method: 'DELETE' }),

        adicionarColaborador: (eventoId, payload) => requisitar(`/eventos/${eventoId}/colaboradores`, { method: 'POST', body: JSON.stringify(payload) }),
        atualizarColaborador: (eventoId, colabId, payload) => requisitar(`/eventos/${eventoId}/colaboradores/${colabId}`, { method: 'PUT', body: JSON.stringify(payload) }),
        removerColaborador: (eventoId, colabId) => requisitar(`/eventos/${eventoId}/colaboradores/${colabId}`, { method: 'DELETE' }),
        verConviteColaborador: (token) => requisitar(`/colaboracoes/${encodeURIComponent(token)}`),
        responderConviteColaborador: (token, status) => requisitar(`/colaboracoes/${encodeURIComponent(token)}/responder`, { method: 'POST', body: JSON.stringify({ status }) }),

        adicionarItemCompartilhado: (eventoId, payload) => requisitar(`/eventos/${eventoId}/itens-compartilhados`, { method: 'POST', body: JSON.stringify(payload) }),
        atualizarItemCompartilhado: (eventoId, itemId, payload) => requisitar(`/eventos/${eventoId}/itens-compartilhados/${itemId}`, { method: 'PUT', body: JSON.stringify(payload) }),
        removerItemCompartilhado: (eventoId, itemId) => requisitar(`/eventos/${eventoId}/itens-compartilhados/${itemId}`, { method: 'DELETE' }),

        adicionarItemEvento: (eventoId, payload) => requisitar(`/eventos/${eventoId}/itens`, { method: 'POST', body: JSON.stringify(payload) }),
        removerItemEvento: (eventoId, itemId) => requisitar(`/eventos/${eventoId}/itens/${itemId}`, { method: 'DELETE' }),
        atualizarTarefa: (eventoId, tarefaId, payload) => requisitar(`/eventos/${eventoId}/tarefas/${tarefaId}`, { method: 'PUT', body: JSON.stringify(payload) }),
        adicionarTarefa: (eventoId, payload) => requisitar(`/eventos/${eventoId}/tarefas`, { method: 'POST', body: JSON.stringify(payload) }),
        removerTarefa: (eventoId, tarefaId) => requisitar(`/eventos/${eventoId}/tarefas/${tarefaId}`, { method: 'DELETE' }),

        listarDespesas: (eventoId) => requisitar(`/eventos/${eventoId}/despesas`),
        adicionarDespesa: (eventoId, payload, chave) => requisitar(`/eventos/${eventoId}/despesas`, { method: 'POST', body: JSON.stringify(payload), headers: chave ? {'Idempotency-Key':chave} : {} }),
        removerDespesa: (eventoId, despesaId) => requisitar(`/eventos/${eventoId}/despesas/${despesaId}`, { method: 'DELETE' }),
        enviarComprovanteDespesa: (eventoId, despesaId, formData) => requisitar(`/eventos/${eventoId}/despesas/${despesaId}/comprovante`, { method: 'POST', body: formData }),
        definirRateio: (eventoId, payload) => requisitar(`/eventos/${eventoId}/rateio`, { method: 'PUT', body: JSON.stringify(payload) }),
        resumoEvento: (eventoId) => requisitar(`/eventos/${eventoId}/resumo`),
        enviarFoto: (eventoId, formData) => requisitar(`/eventos/${eventoId}/fotos`, { method: 'POST', body: formData }),
        removerFoto: (eventoId, fotoId) => requisitar(`/eventos/${eventoId}/fotos/${fotoId}`, { method: 'DELETE' }),

        notificacoes: () => requisitar('/notificacoes'),
        marcarNotificacoesLidas: () => requisitar('/notificacoes/lidas', { method: 'PUT' }),
        favoritos: () => requisitar('/favoritos'),
        alternarFavorito: (chave) => requisitar('/favoritos', { method: 'POST', body: JSON.stringify({ chave }) }),

        fornecedores: (params = '') => requisitar('/fornecedores' + params),
        fornecedoresPerto: (params = {}) => {
            const query = new URLSearchParams(
                Object.fromEntries(Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== ''))
            ).toString();
            return requisitar('/catalogo/perto?' + query);
        },

        verRsvp: (token) => requisitar('/rsvp/' + encodeURIComponent(token)),
        responderRsvp: (token, payload) => requisitar('/rsvp/' + encodeURIComponent(token), { method: 'POST', body: JSON.stringify(payload) }),
        assumirItemRsvp: (token, itemId) => requisitar(`/rsvp/${encodeURIComponent(token)}/itens/${itemId}/assumir`, { method: 'POST' }),
        liberarItemRsvp: (token, itemId) => requisitar(`/rsvp/${encodeURIComponent(token)}/itens/${itemId}/liberar`, { method: 'POST' })
    };
})();
