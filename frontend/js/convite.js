(function () {
    const token = new URLSearchParams(location.search).get('token');
    const $ = (id) => document.getElementById(id);
    const dataBR = (iso) => iso ? new Date(iso + 'T12:00:00').toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' }) : '—';
    if (!token) { $('conviteCarregando').textContent = 'Convite inválido.'; return; }

    let convite = null;
    let usuario = null;
    async function carregar() {
        try {
            convite = await MomentusAPI.verConviteColaborador(token);
            try { usuario = (await MomentusAPI.me()).usuario; } catch (_) { usuario = null; }
            $('conviteCarregando').hidden = true; $('conviteConteudo').hidden = false;
            $('conviteOrganizador').textContent = convite.evento.organizador;
            $('conviteEvento').textContent = convite.evento.nome;
            $('conviteData').textContent = dataBR(convite.evento.data);
            $('conviteEmail').textContent = convite.colaborador.email;
            const next = encodeURIComponent('convite.html?token=' + token);
            $('linkEntrarConvite').href = 'index.html?next=' + next;
            $('linkCriarConvite').href = 'cadastro.html?tipo=cliente&next=' + next;

            if (convite.colaborador.status !== 'pendente') {
                $('conviteRespondido').hidden = false;
                $('conviteRespondido').innerHTML = `<strong>Convite ${convite.colaborador.status === 'ativo' ? 'aceito' : 'recusado'}.</strong><span>${convite.colaborador.status === 'ativo' ? 'O evento já está disponível na sua conta.' : 'Sua resposta foi registrada.'}</span>`;
                return;
            }
            if (!usuario) { $('conviteLoginNecessario').hidden = false; return; }
            if (String(usuario.email).toLowerCase() !== String(convite.colaborador.email).toLowerCase()) {
                $('conviteLoginNecessario').hidden = false;
                $('conviteLoginNecessario').querySelector('strong').textContent = 'Você entrou com outro e-mail.';
                return;
            }
            $('conviteAcoes').hidden = false;
        } catch (e) { $('conviteCarregando').textContent = e.message; }
    }

    async function responder(status) {
        $('conviteErro').textContent = '';
        $('aceitarConvite').disabled = $('recusarConvite').disabled = true;
        try {
            await MomentusAPI.responderConviteColaborador(token, status);
            $('conviteAcoes').hidden = true; $('conviteRespondido').hidden = false;
            $('conviteRespondido').innerHTML = `<strong>${status === 'ativo' ? 'Colaboração aceita!' : 'Convite recusado.'}</strong><span>${status === 'ativo' ? '<a href="inicio.html">Abrir meus eventos →</a>' : 'Sua resposta foi registrada.'}</span>`;
        } catch (e) { $('conviteErro').textContent = e.message; $('aceitarConvite').disabled = $('recusarConvite').disabled = false; }
    }
    $('aceitarConvite').addEventListener('click', () => responder('ativo'));
    $('recusarConvite').addEventListener('click', () => responder('recusado'));
    carregar();
})();
