(function () {
    window.addEventListener('hashchange', () => location.reload());
    const token = new URLSearchParams(location.hash.slice(1)).get('token') || new URLSearchParams(location.search).get('token');
    const $ = id => document.getElementById(id);
    const retorno = 'convite.html#token=' + encodeURIComponent(token || '');
    const entrada = 'index.html?next=' + encodeURIComponent(retorno);
    $('linkEntrarConvite').href = entrada;
    $('linkCriarConvite').href = 'cadastro.html?next=' + encodeURIComponent(retorno);

    let convite = null, usuario = null, enviando = false, acessoAoEvento = false;

    function mostrarErroCarregamento(mensagem) {
        $('conviteCarregando').hidden = true;
        $('conviteConteudo').hidden = true;
        $('conviteErroCarregamento').hidden = false;
        $('conviteErroMensagem').textContent = mensagem;
        $('tentarConviteNovamente').hidden = !token;
    }

    function mostrarAcesso() {
        const outraConta = !!usuario;
        const aceito = convite.colaborador.status === 'ativo';
        $('conviteLoginNecessario').hidden = false;
        $('conviteTituloAcesso').textContent = outraConta ? 'Você está usando outro e-mail.'
            : aceito ? 'Entre para acessar o evento' : 'Entre para responder ao convite';
        $('conviteTextoAcesso').textContent = outraConta
            ? `Sua conta atual é ${usuario.email}. Use uma conta com o e-mail ${convite.colaborador.email}.`
            : 'Se ainda não tiver conta, cadastre-se com o e-mail deste convite. Você voltará para esta página.';
        $('linkEntrarConvite').hidden = outraConta;
        $('linkCriarConvite').hidden = outraConta;
        $('trocarContaConvite').hidden = !outraConta;
    }

    function renderizar() {
        const emailCorreto = usuario && usuario.email.toLowerCase() === convite.colaborador.email.toLowerCase();
        const status = convite.colaborador.status;
        $('conviteCarregando').hidden = true;
        $('conviteErroCarregamento').hidden = true;
        $('conviteConteudo').hidden = false;
        $('conviteOrganizador').textContent = convite.evento.organizador;
        $('conviteEvento').textContent = convite.evento.nome;
        $('conviteData').textContent = MomentusUtils.dataPorExtenso(convite.evento.data);
        $('conviteHora').textContent = convite.evento.hora || 'A combinar';
        $('conviteEmail').textContent = convite.colaborador.email;
        $('conviteAcoes').hidden = true;
        $('conviteLoginNecessario').hidden = true;
        $('conviteRespondido').hidden = true;
        if (status === 'pendente') {
            if (emailCorreto) $('conviteAcoes').hidden = false;
            else mostrarAcesso();
            return;
        }

        const resposta = $('conviteRespondido');
        const titulo = document.createElement('strong');
        const descricao = document.createElement('span');
        titulo.textContent = status === 'ativo' ? 'Colaboração aceita!' : 'Convite recusado.';
        descricao.textContent = status === 'ativo'
            ? 'O evento está disponível na conta convidada. Sua participação já foi atualizada para o responsável.'
            : 'A resposta foi registrada. O responsável pelo evento pode acompanhar pela lista de colaboradores.';
        resposta.replaceChildren(titulo, descricao);
        resposta.hidden = false;
        if (status === 'ativo' && acessoAoEvento) {
            const abrir = document.createElement('a');
            abrir.href = 'evento.html?id=' + encodeURIComponent(convite.evento.id);
            abrir.textContent = 'Abrir evento →';
            resposta.appendChild(abrir);
        } else if (status === 'ativo') mostrarAcesso();
    }

    async function carregar() {
        if (!token) { mostrarErroCarregamento('Este link não contém um convite. Peça ao responsável para compartilhar o link completo.'); return; }
        $('conviteCarregando').hidden = false;
        $('conviteErroCarregamento').hidden = true;
        $('conviteConteudo').hidden = true;
        try {
            convite = await MomentusAPI.verConviteColaborador(token);
            try { usuario = (await MomentusAPI.me()).usuario; }
            catch (erro) { if (erro.status !== 401) throw erro; usuario = null; }
            acessoAoEvento = false;
            if (usuario && convite.colaborador.status === 'ativo') {
                // Depois do aceite, o vínculo é com a conta, mesmo que ela
                // atualize seu e-mail. A API confirma a permissão de acesso.
                try { await MomentusAPI.buscarEvento(convite.evento.id); acessoAoEvento = true; }
                catch (erro) { if (![401, 403, 404].includes(erro.status)) throw erro; }
            }
            renderizar();
        } catch (erro) { mostrarErroCarregamento(erro.message); }
    }

    async function responder(status) {
        if (enviando) return;
        enviando = true;
        $('conviteErro').textContent = '';
        $('aceitarConvite').disabled = $('recusarConvite').disabled = true;
        try {
            const resposta = await MomentusAPI.responderConviteColaborador(token, status);
            convite.colaborador.status = resposta.status;
            acessoAoEvento = resposta.status === 'ativo';
            renderizar();
        } catch (erro) { $('conviteErro').textContent = erro.message; }
        finally {
            enviando = false;
            $('aceitarConvite').disabled = $('recusarConvite').disabled = false;
        }
    }

    $('trocarContaConvite').addEventListener('click', async () => {
        if (enviando) return;
        enviando = true;
        $('trocarContaConvite').disabled = true;
        $('conviteErro').textContent = '';
        try {
            await MomentusAPI.logout();
            location.href = entrada;
        } catch (erro) {
            $('conviteErro').textContent = erro.message;
            $('trocarContaConvite').disabled = false;
            enviando = false;
        }
    });
    $('aceitarConvite').addEventListener('click', () => responder('ativo'));
    $('recusarConvite').addEventListener('click', () => responder('recusado'));
    $('tentarConviteNovamente').addEventListener('click', carregar);
    carregar();
})();
