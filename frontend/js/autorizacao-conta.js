(() => {
    const $ = id => document.getElementById(id);
    const status = $('statusAutorizacaoConta');
    if (!status) return;
    async function atualizar() {
        try {
            const registro = await MomentusAPI.requisitar('/privacidade/autorizacao');
            $('formDeclararIdade').hidden = registro.status !== 'nao_informado';
            $('gerarLinkResponsavel').hidden = registro.faixa_etaria !== 'menor' || registro.status === 'autorizado';
            $('revogarAutorizacaoConta').hidden = registro.faixa_etaria !== 'menor' || registro.status !== 'autorizado';
            const textos = {nao_informado:'Registre sua declaração de idade para continuar.',pendente:'A conta aguarda a autorização do responsável.',revogado:'A autorização foi revogada. O acesso a eventos está suspenso.',negado:'O responsável não autorizou o uso da conta.',autorizado:registro.faixa_etaria === 'adulto' ? 'Declaração registrada: 18 anos ou mais.' : 'Autorização do responsável registrada.'};
            status.textContent = textos[registro.status] || 'Declaração pendente.';
        } catch (erro) {status.textContent=erro.message;}
    }
    $('formDeclararIdade').addEventListener('submit', async e => {
        e.preventDefault();e.submitter.disabled=true;
        try {
            await MomentusAPI.requisitar('/privacidade/autorizacao',{method:'PUT',body:JSON.stringify({faixa_etaria:$('faixaEtariaConfig').value,declaracao_idade:true})});
            await Momentus.sincronizarPerfil();await atualizar();
        } catch (erro) {status.textContent=erro.message;}
        finally {e.submitter.disabled=false;}
    });
    $('gerarLinkResponsavel').addEventListener('click', async e => {
        e.currentTarget.disabled=true;
        try {
            const resposta=await MomentusAPI.requisitar('/privacidade/autorizacao/link',{method:'POST'});
            $('urlResponsavelConta').value=new URL(resposta.link,location.origin).href;
            $('linkResponsavelConta').hidden=false;
        } catch (erro) {status.textContent=erro.message;}
        finally {$('gerarLinkResponsavel').disabled=false;}
    });
    $('copiarLinkResponsavelConta').addEventListener('click', async () => {
        try {await navigator.clipboard.writeText($('urlResponsavelConta').value);status.textContent='Link copiado. Envie somente ao responsável legal.';}
        catch (_) {$('urlResponsavelConta').select();status.textContent='Selecione e copie o link para compartilhar com o responsável.';}
    });
    $('revogarAutorizacaoConta').addEventListener('click', async () => {
        if (!confirm('Revogar a autorização e suspender o acesso desta conta aos eventos?')) return;
        try {await MomentusAPI.requisitar('/privacidade/autorizacao',{method:'DELETE'});await atualizar();await Momentus.sincronizarPerfil();}
        catch (erro) {status.textContent=erro.message;}
    });
    document.addEventListener('visibilitychange',()=>{if(!document.hidden){atualizar();Momentus.sincronizarPerfil();}});
    atualizar();
})();
