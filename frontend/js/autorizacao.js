(() => {
    window.addEventListener('hashchange', () => location.reload());
    const $ = id => document.getElementById(id);
    const params=new URLSearchParams(location.hash.slice(1));
    const segredo={tipo:params.get('tipo'),token:params.get('token')};
    history.replaceState(null,'',location.pathname);
    let versao;
    MomentusAPI.requisitar('/autorizacoes/consultar',{method:'POST',body:JSON.stringify(segredo)}).then(info=>{
        versao=info.versao;
        $('titularAutorizacao').textContent=`Titular: ${info.nome}${info.evento ? ' · Evento: '+info.evento : ''}`;
        const conta=info.tipo==='conta';
        $('decisaoConta').hidden=!conta;$('decisaoSaude').hidden=conta;
        document.querySelectorAll('[name="decisao"]').forEach(input=>{input.required=conta;input.disabled=!conta;});
        document.querySelectorAll('[name="participacao"]').forEach(input=>{input.required=!conta;input.disabled=conta;});
        $('formAutorizacao').hidden=false;$('statusAutorizacao').textContent='Este link permite uma única resposta e não substitui os documentos disponíveis para leitura.';
    }).catch(erro=>{$('statusAutorizacao').textContent=erro.message;});
    $('autorizarSaudeResponsavel').addEventListener('change',e=>{
        $('campoSaudeResponsavel').hidden=!e.target.checked;$('saudeResponsavel').required=e.target.checked;
        if(!e.target.checked)$('saudeResponsavel').value='';
    });
    document.querySelectorAll('[name="participacao"]').forEach(radio=>radio.addEventListener('change',()=>{
        const sim=document.querySelector('[name="participacao"]:checked')?.value==='sim';
        $('autorizarSaudeResponsavel').disabled=!sim;
        if(!sim){$('autorizarSaudeResponsavel').checked=false;$('saudeResponsavel').value='';$('campoSaudeResponsavel').hidden=true;$('saudeResponsavel').required=false;}
    }));
    $('formAutorizacao').addEventListener('submit',async e=>{
        e.preventDefault();e.submitter.disabled=true;
        try {
            const payload={...segredo,responsavel_nome:$('responsavelNome').value.trim(),responsavel_email:$('responsavelEmail').value.trim(),vinculo:$('responsavelVinculo').value.trim(),declaracao_responsavel:$('declaracaoResponsavel').checked,versao_consentimento:versao};
            if(segredo.tipo==='conta')payload.autorizar_conta=document.querySelector('[name="decisao"]:checked')?.value==='sim';
            else {payload.autorizar_participacao=document.querySelector('[name="participacao"]:checked')?.value==='sim';payload.autorizar_saude=payload.autorizar_participacao && $('autorizarSaudeResponsavel').checked;payload.saude=payload.autorizar_saude ? $('saudeResponsavel').value.trim() : '';}
            const resposta=await MomentusAPI.requisitar('/autorizacoes/responder',{method:'POST',body:JSON.stringify(payload)});
            $('formAutorizacao').reset();$('formAutorizacao').hidden=true;$('statusAutorizacao').textContent=resposta.mensagem;
        } catch(erro){$('statusAutorizacao').textContent=erro.message;e.submitter.disabled=false;}
    });
})();
