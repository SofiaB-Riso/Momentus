(() => {
    MomentusAPI.requisitar('/privacidade/info').then(info => {
        document.querySelectorAll('[data-versao-termos]').forEach(el => { el.textContent = info.versao; });
        const campos = {responsavelPrivacidade: 'responsavel', encarregadoPrivacidade: 'encarregado', emailPrivacidade: 'email', telefonePrivacidade: 'telefone'};
        Object.entries(campos).forEach(([id, chave]) => {
            const el = document.getElementById(id);
            if (el) el.textContent = info[chave] || 'Ainda não informado pelo responsável pelo projeto.';
        });
        const aviso=document.getElementById('statusContatoPrivacidade');
        if(aviso)aviso.textContent=info.demonstracao ? 'Contatos de demonstração acadêmica. Este ambiente não oferece atendimento real por e-mail.' : '';
    }).catch(() => {
        const el = document.getElementById('statusContatoPrivacidade');
        if (el) el.textContent = 'Não foi possível carregar o contato agora. Tente novamente mais tarde.';
    });
})();
