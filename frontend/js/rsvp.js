(function () {
    const token = new URLSearchParams(location.search).get('token');
    const $ = (id) => document.getElementById(id);
    const formatarData = (iso) => iso ? new Date(iso + 'T12:00:00').toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' }) : '—';
    const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    let dadosAtuais = null;
    if (!token) { $('rsvpCarregando').textContent = 'Link de convite inválido.'; return; }

    function renderItens() {
        const itens = (dadosAtuais && dadosAtuais.evento.itens_compartilhados) || [];
        const sec = $('rsvpItensCompartilhados');
        if (!itens.length) { sec.hidden = true; return; }
        sec.hidden = false;
        $('rsvpListaItens').innerHTML = itens.map((i) => {
            const meu = i.responsavelTipo === 'convidado' && String(i.responsavelId) === String(dadosAtuais.convidado.id);
            const livre = !i.responsavelNome;
            return `<div class="itemPublicoRsvp"><div><strong>${esc(i.nome)}</strong><small>Quantidade: ${Number(i.quantidade || 1)}</small>${i.responsavelNome ? `<span>${meu ? 'Você ficou responsável' : `Responsável: ${esc(i.responsavelNome)}`}</span>` : '<span>Disponível</span>'}</div>${livre || meu ? `<button data-item="${i.id}" data-acao="${meu ? 'liberar' : 'assumir'}">${meu ? 'Liberar' : 'Eu levo'}</button>` : ''}</div>`;
        }).join('');
        $('rsvpListaItens').querySelectorAll('[data-item]').forEach((b) => b.addEventListener('click', async () => {
            b.disabled = true;
            try {
                if (b.dataset.acao === 'assumir') await MomentusAPI.assumirItemRsvp(token, b.dataset.item);
                else await MomentusAPI.liberarItemRsvp(token, b.dataset.item);
                dadosAtuais = await MomentusAPI.verRsvp(token); renderItens();
            } catch (e) { $('rsvpErro').textContent = e.message; }
            finally { b.disabled = false; }
        }));
    }

    MomentusAPI.verRsvp(token).then((r) => {
        dadosAtuais = r;
        $('rsvpCarregando').hidden = true; $('rsvpConteudo').hidden = false;
        $('rsvpNome').textContent = r.convidado.nome; $('rsvpEvento').textContent = r.evento.nome;
        $('rsvpData').textContent = formatarData(r.evento.data); $('rsvpHora').textContent = r.evento.hora || 'A combinar';
        $('rsvpLocal').textContent = r.evento.local || 'Local a confirmar'; $('rsvpOrganizador').textContent = r.evento.organizador || 'Momentus';
        const publicos = r.evento.confirmados_publicos || [];
        if (publicos.length) { $('rsvpConfirmadosPublicos').hidden = false; $('rsvpConfirmadosPublicos').innerHTML = `<small>Quem já confirmou</small><p>${publicos.map(esc).join(' · ')}</p>`; }
        $('rsvpRestricoes').value = r.convidado.restricoes || '';
        const radio = document.querySelector(`input[name="status"][value="${r.convidado.status}"]`); if (radio) radio.checked = true;
        renderItens();
    }).catch((e) => { $('rsvpCarregando').textContent = e.message; });

    $('formRsvp').addEventListener('submit', async (e) => {
        e.preventDefault(); $('rsvpErro').textContent = '';
        const selecionado = document.querySelector('input[name="status"]:checked'); if (!selecionado) return;
        const botao = e.submitter; botao.disabled = true;
        try { await MomentusAPI.responderRsvp(token, { status: selecionado.value, restricoes: $('rsvpRestricoes').value.trim() }); $('rsvpSucesso').hidden = false; $('rsvpSucesso').scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
        catch (erro) { $('rsvpErro').textContent = erro.message; } finally { botao.disabled = false; }
    });
})();
