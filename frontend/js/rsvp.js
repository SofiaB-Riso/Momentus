(function () {
    const token = new URLSearchParams(location.search).get('token');
    const $ = id => document.getElementById(id);
    const esc = MomentusUtils.escapeHTML;
    const formatarData = MomentusUtils.dataPorExtenso;
    let dadosAtuais = null, editando = false, carregando = false, aguardando = false, fluxo = null, revisao = null;
    if (!token) { $('rsvpCarregando').textContent='Link de convite inválido.'; return; }

    function renderizar(r) {
        dadosAtuais=r;
        $('rsvpCarregando').hidden=true; $('rsvpConteudo').hidden=false;
        $('rsvpNome').textContent=r.convidado.nome; $('rsvpEvento').textContent=r.evento.nome;
        $('rsvpData').textContent=formatarData(r.evento.data); $('rsvpHora').textContent=r.evento.hora || 'A combinar';
        $('rsvpLocal').textContent=[r.evento.local,r.evento.cidade].filter(Boolean).join(', ') || 'Local a confirmar';
        $('rsvpOrganizador').textContent=r.evento.organizador;
        const mapas=r.evento.mapas || {};
        $('rsvpMapas').innerHTML=mapas.google ? `<a class="botaoSecundario" href="${esc(mapas.google)}" target="_blank" rel="noopener">Google Maps ↗</a><a class="botaoSecundario" href="${esc(mapas.waze)}" target="_blank" rel="noopener">Waze ↗</a>` : '';
        const publicos=r.evento.confirmados_publicos || [];
        $('rsvpConfirmadosPublicos').hidden=!publicos.length;
        $('rsvpConfirmadosPublicos').innerHTML=`<small>Quem já confirmou</small><p>${publicos.map(esc).join(' · ')}</p>`;
        if (!editando) {
            $('rsvpRestricoes').value=r.convidado.restricoes || '';
            const radio=document.querySelector(`input[name="status"][value="${r.convidado.status}"]`);
            if(radio) radio.checked=true;
        }
        const avisos=r.avisos || [];
        $('rsvpAvisos').hidden=!avisos.length;
        $('rsvpListaAvisos').innerHTML=avisos.slice(0,5).map(a=>`<li><strong>${esc(a.titulo)}</strong><p>${esc(a.mensagem)}</p></li>`).join('');
        const itens=r.evento.itens_compartilhados || [];
        $('rsvpItensCompartilhados').hidden=!itens.length;
        $('rsvpListaItens').innerHTML=itens.map(i=>{
            const meu=i.responsavelTipo==='convidado' && String(i.responsavelId)===String(r.convidado.id);
            const livre=!i.responsavelNome;
            const podeAssumir=livre && r.convidado.status!=='recusado';
            return `<div class="itemPublicoRsvp"><div><strong>${esc(i.nome)}</strong><small>Quantidade: ${Number(i.quantidade)}</small><span>${meu ? 'Você ficou responsável' : livre ? 'Disponível' : 'Já reservado'}</span></div>${podeAssumir || meu ? `<button data-item="${i.id}" data-acao="${meu?'liberar':'assumir'}">${meu?'Liberar':'Eu levo'}</button>`:''}</div>`;
        }).join('');
        $('rsvpListaItens').querySelectorAll('[data-item]').forEach(b=>b.addEventListener('click',async()=>{
            b.disabled=true; $('rsvpErro').textContent='';
            try {
                if(b.dataset.acao==='assumir') await MomentusAPI.assumirItemRsvp(token,b.dataset.item);
                else await MomentusAPI.liberarItemRsvp(token,b.dataset.item);
            } catch(e) { $('rsvpErro').textContent=e.message; }
            finally { await atualizar(); b.disabled=false; }
        }));
    }

    async function atualizar() {
        if(document.hidden) return;
        if(carregando) { aguardando=true; return; }
        carregando=true;
        try { renderizar(await MomentusAPI.verRsvp(token)); }
        catch(e) {
            if(dadosAtuais) $('rsvpErro').textContent=e.message;
            else $('rsvpCarregando').textContent=e.message;
            if(e.status===404) { fluxo?.close(); fluxo=null; $('formRsvp').hidden=true; $('rsvpItensCompartilhados').hidden=true; }
        } finally {
            carregando=false;
            if(aguardando) { aguardando=false; await atualizar(); }
        }
    }

    $('formRsvp').addEventListener('input',()=>{editando=true; $('rsvpSucesso').hidden=true;});
    $('formRsvp').addEventListener('submit',async e=>{
        e.preventDefault(); $('rsvpErro').textContent='';
        const selecionado=document.querySelector('input[name="status"]:checked'); if(!selecionado) return;
        const botao=e.submitter; botao.disabled=true;
        try {
            await MomentusAPI.responderRsvp(token,{status:selecionado.value,restricoes:$('rsvpRestricoes').value.trim()});
            editando=false; await atualizar(); $('rsvpSucesso').hidden=false;
            $('rsvpSucesso').scrollIntoView({behavior:'smooth',block:'nearest'});
        } catch(e) { $('rsvpErro').textContent=e.message; } finally {botao.disabled=false;}
    });

    function conectar() {
        if(fluxo || document.hidden || !window.EventSource) return;
        fluxo=new EventSource(`/rsvp/${encodeURIComponent(token)}/atualizacoes`);
        fluxo.addEventListener('alteracao',e=>{const nova=JSON.parse(e.data).revisao;if(nova!==revisao){revisao=nova;atualizar();}});
        fluxo.addEventListener('encerrado',()=>{fluxo.close();fluxo=null;atualizar();});
    }
    atualizar().then(()=>{if(dadosAtuais) conectar();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden){fluxo?.close();fluxo=null;}else{atualizar();conectar();}});
    window.addEventListener('pagehide',()=>fluxo?.close());
    setInterval(atualizar,15000);
})();
