(function () {
    window.addEventListener('hashchange', () => location.reload());
    const token = new URLSearchParams(location.hash.slice(1)).get('token') || new URLSearchParams(location.search).get('token');
    const $ = id => document.getElementById(id);
    const esc = MomentusUtils.escapeHTML;
    const formatarData = MomentusUtils.dataPorExtenso;
    let dadosAtuais = null, editando = false, carregando = false, aguardando = false, fluxo = null, revisao = null;
    function indisponivel(mensagem) {
        $('rsvpTituloEstado').textContent = 'Não foi possível abrir o convite';
        $('rsvpCarregando').textContent = mensagem;
        $('rsvpVoltar').hidden = false;
    }
    if (!token) { indisponivel('Este link não contém um convite. Peça a quem organiza o evento para compartilhar o link completo.'); return; }

    function renderizar(r) {
        dadosAtuais=r;
        const fila = r.lista_espera || {};
        $('rsvpVagas').hidden = fila.limite_vagas == null && r.convidado.status !== 'espera';
        $('rsvpVagas').textContent = r.convidado.status === 'espera'
            ? 'Você está na lista de espera'+(fila.posicao ? ', posição '+fila.posicao : '')+'. Uma desistência confirma automaticamente a próxima pessoa. Acompanhe este convite.'
            : fila.limite_vagas != null ? 'Vagas confirmadas: '+fila.confirmados+' de '+fila.limite_vagas+'. Ao atingir o limite, novas confirmações entram na lista de espera.' : '';
        $('rsvpSucesso').querySelector('strong').textContent = r.convidado.status === 'espera' ? 'Você está na lista de espera' : 'Presença atualizada!';
        $('rsvpSucesso').querySelector('span').textContent = r.convidado.status === 'espera'
            ? 'Sua solicitação foi registrada. Acompanhe sua posição e a liberação da vaga neste convite.'
            : 'Sua resposta já apareceu para quem está organizando o evento.';
        $('rsvpEstado').hidden=true; $('rsvpConteudo').hidden=false;
        $('rsvpNome').textContent=r.convidado.nome; $('rsvpEvento').textContent=r.evento.nome;
        $('rsvpData').textContent=formatarData(r.evento.data); $('rsvpHora').textContent=r.evento.hora || 'A combinar';
        $('rsvpLocal').textContent=[r.evento.local,r.evento.cidade].filter(Boolean).join(', ') || 'Local a confirmar';
        $('rsvpOrganizador').textContent=r.evento.organizador;
        const mapas=r.evento.mapas || {};
        $('rsvpMapas').innerHTML=mapas.google ? `<a class="botaoSecundario" href="${esc(mapas.google)}" target="_blank" rel="noopener">Google Maps ↗</a>` : '';
        const publicos=r.evento.confirmados_publicos || [];
        $('rsvpConfirmadosPublicos').hidden=!publicos.length;
        $('rsvpConfirmadosPublicos').innerHTML=`<small>Quem já confirmou</small><p>${publicos.map(esc).join(' · ')}</p>`;
        if (!editando) {
            $('rsvpRestricoes').value=r.convidado.preferencias_alimentares || '';
            $('rsvpPreferenciasSemSaude').checked=!!$('rsvpRestricoes').value;
            $('rsvpSaude').value=r.convidado.informacoes_saude || '';
            $('rsvpAutorizarSaude').checked=!!r.convidado.consentimento?.autorizado;
            $('rsvpFaixaEtaria').value=r.convidado.consentimento?.faixa_etaria || '';
            atualizarCamposSaude();
            const radio=document.querySelector(`input[name="status"][value="${r.convidado.status === 'espera' ? 'confirmado' : r.convidado.status}"]`);
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
            const podeAssumir=livre && !['recusado','espera'].includes(r.convidado.status);
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
            else indisponivel(e.message);
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
            const payload={status:selecionado.value,restricoes:$('rsvpRestricoes').value.trim(),preferencias_sem_saude:$('rsvpPreferenciasSemSaude').checked};
            if($('rsvpFaixaEtaria').value)payload.faixa_etaria=$('rsvpFaixaEtaria').value;
            if(payload.faixa_etaria==='adulto')Object.assign(payload,{saude:$('rsvpAutorizarSaude').checked ? $('rsvpSaude').value.trim() : '',autorizar_saude:$('rsvpAutorizarSaude').checked,versao_consentimento:dadosAtuais.versao_consentimento});
            await MomentusAPI.responderRsvp(token,payload);
            editando=false; await atualizar(); $('rsvpSucesso').hidden=false;
            $('rsvpSucesso').scrollIntoView({behavior:'smooth',block:'nearest'});
        } catch(e) { $('rsvpErro').textContent=e.message; } finally {botao.disabled=false;}
    });

    function atualizarCamposSaude() {
        const adulto=$('rsvpFaixaEtaria').value==='adulto';
        $('rsvpSaudeAdulto').hidden=!adulto;
        $('rsvpSaudeMenor').hidden=$('rsvpFaixaEtaria').value!=='menor';
        $('campoSaudeRsvp').hidden=!adulto || !$('rsvpAutorizarSaude').checked;
        $('rsvpSaude').required=adulto && $('rsvpAutorizarSaude').checked;
        $('rsvpPreferenciasSemSaude').required=!!$('rsvpRestricoes').value.trim();
    }
    ['rsvpFaixaEtaria','rsvpAutorizarSaude','rsvpRestricoes'].forEach(id=>$(id).addEventListener('input',atualizarCamposSaude));
    $('rsvpGerarResponsavel').addEventListener('click',async e=>{
        e.currentTarget.disabled=true;
        try {
            const resposta=await MomentusAPI.requisitar(`/rsvp/${encodeURIComponent(token)}/responsavel`,{method:'POST'});
            $('rsvpLinkResponsavel').value=new URL(resposta.link,location.origin).href;
            $('rsvpCompartilharResponsavel').hidden=false;
        } catch(erro){$('rsvpErro').textContent=erro.message;}
        finally {$('rsvpGerarResponsavel').disabled=false;}
    });
    $('rsvpCopiarResponsavel').addEventListener('click',async()=>{
        try {await navigator.clipboard.writeText($('rsvpLinkResponsavel').value);$('rsvpErro').textContent='Link copiado. Compartilhe somente com o responsável legal.';}
        catch(_) {$('rsvpLinkResponsavel').select();}
    });
    $('rsvpRevogarSaude').addEventListener('click',async()=>{
        if(!confirm('Apagar as informações de saúde e revogar essa autorização?'))return;
        try {await MomentusAPI.responderRsvp(token,{status:dadosAtuais.convidado.status === 'espera' ? 'confirmado' : dadosAtuais.convidado.status,revogar_saude:true});editando=false;await atualizar();}
        catch(erro){$('rsvpErro').textContent=erro.message;}
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
