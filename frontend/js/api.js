const API_BASE_URL = 'http://127.0.0.1:5000';

const MomentusAPI = (() => {

    async function requisitar(caminho, opcoes) {
        let resposta;
        try {
            resposta = await fetch(API_BASE_URL + caminho, Object.assign({
                headers: { 'Content-Type': 'application/json' }
            }, opcoes));
        } catch (erroDeRede) {
            const erro = new Error('Não foi possível conectar ao servidor. Verifique se o backend está rodando em ' + API_BASE_URL + '.');
            erro.semConexao = true;
            throw erro;
        }

        if (resposta.status === 204) return null;

        let corpo = null;
        try { corpo = await resposta.json(); } catch (e) { corpo = null; }

        if (!resposta.ok) {
            const mensagem = (corpo && corpo.erro) ? corpo.erro : 'Ocorreu um erro ao falar com o servidor.';
            const erro = new Error(mensagem);
            erro.status = resposta.status;
            throw erro;
        }

        return corpo;
    }

    return {
        listarEventos() {
            return requisitar('/eventos');
        },
        criarEvento(payload) {
            return requisitar('/eventos', { method: 'POST', body: JSON.stringify(payload) });
        },
        atualizarEvento(id, payload) {
            return requisitar('/eventos/' + encodeURIComponent(id), { method: 'PUT', body: JSON.stringify(payload) });
        },
        removerEvento(id) {
            return requisitar('/eventos/' + encodeURIComponent(id), { method: 'DELETE' });
        }
    };
})();
