(() => {
    const arquivo = document.getElementById('arquivoAvatarConfig');
    const remover = document.getElementById('removerAvatarConfig');
    const status = document.getElementById('statusAvatarConfig');
    const editar = document.querySelector('.editarAvatar');
    function atualizarFoto() {
        const perfil = Momentus.obterPerfil();
        const foto = document.getElementById('fotoAvatarConfig');
        const iniciais = document.getElementById('iniciaisAvatarConfig');
        iniciais.textContent = Momentus.iniciais(perfil.nome);
        foto.hidden = !perfil.foto_url; iniciais.hidden = !!perfil.foto_url; remover.hidden = !perfil.foto_url;
        if (perfil.foto_url) foto.src = perfil.foto_url; else foto.removeAttribute('src');
    }
    document.addEventListener('momentus:perfil-alterado', atualizarFoto);
    atualizarFoto();
    editar.addEventListener('click', () => arquivo.click());
    async function alterarFoto(opcoes) {
        editar.disabled = true; remover.disabled = true;
        try {
            await MomentusAPI.requisitar('/auth/foto', opcoes);
            await Momentus.sincronizarPerfil();
            status.textContent = opcoes.method === 'DELETE' ? 'Foto removida.' : 'Foto atualizada.';
        } catch (erro) { status.textContent = erro.message; }
        finally { editar.disabled = false; remover.disabled = false; arquivo.value = ''; }
    }
    arquivo.addEventListener('change', () => {
        if (!arquivo.files[0]) return;
        if (arquivo.files[0].size > 8 * 1024 * 1024) { status.textContent = 'Selecione uma imagem de até 8 MB.'; arquivo.value = ''; return; }
        const dados = new FormData(); dados.append('foto', arquivo.files[0]);
        alterarFoto({method: 'POST', body: dados});
    });
    remover.addEventListener('click', () => alterarFoto({method: 'DELETE'}));

    const form = document.getElementById('formAceiteConfig');
    const statusAceite = document.getElementById('statusAceiteConfig');
    let versao;
    async function carregarAceite() {
        try {
            const info = await MomentusAPI.requisitar('/privacidade/info'); versao = info.versao;
            if (info.aceite && info.aceite.versao === info.versao) {
                statusAceite.textContent = `Termos na versão ${info.aceite.versao} aceitos em ${new Date(info.aceite.aceito_em).toLocaleString('pt-BR')}.`;
                form.hidden = true;
            } else {
                statusAceite.textContent = 'Ainda não há registro de aceite da versão atual para esta conta.';
                form.hidden = false;
            }
        } catch (erro) { statusAceite.textContent = erro.message; }
    }
    form.addEventListener('submit', async evento => {
        evento.preventDefault(); const botao = form.querySelector('button'); botao.disabled = true;
        try {
            await MomentusAPI.requisitar('/privacidade/aceite', {method: 'POST', body: JSON.stringify({aceite_termos: document.getElementById('aceiteTermosConfig').checked, versao_termos: versao})});
            await carregarAceite();
        } catch (erro) { statusAceite.textContent = erro.message; }
        finally { botao.disabled = false; }
    });
    carregarAceite();
    document.getElementById('limparLocalizacaoConfig').addEventListener('click', () => {
        localStorage.removeItem('momentus_localizacao_fornecedores');
        localStorage.setItem('momentus:localizacao-desativada', 'sim');
        document.getElementById('statusPrivacidadeConfig').textContent = 'Localização salva apagada. A busca automática ficará desativada até você usar o botão de localização novamente.';
    });
})();
