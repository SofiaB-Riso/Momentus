(function () {
    const params = new URLSearchParams(location.search);

    function destino(usuario) {
        if (usuario.autorizacao_conta?.status !== 'autorizado') return 'configuracoes.html#autorizacaoContaConfig';
        const proximo = params.get('next');
        if (proximo) {
            try {
                const url = new URL(proximo, location.origin);
                const paginas = ['inicio.html', 'eventos.html', 'evento.html', 'planejar.html', 'catalogo.html', 'configuracoes.html', 'convite.html'];
                if (url.origin === location.origin && paginas.includes(url.pathname.slice(1))) return url.pathname + url.search + url.hash;
            } catch (_) { /* Um destino inválido volta à página inicial. */ }
        }
        return 'inicio.html';
    }

    MomentusAPI.me().then((r) => {
        if (r && r.usuario) location.href = destino(r.usuario);
    }).catch(() => {});

    const formLogin = document.getElementById('formLogin');
    if (formLogin) {
        const erro = document.getElementById('erroLogin');
        const botao = formLogin.querySelector('button[type="submit"]');
        formLogin.addEventListener('submit', async (e) => {
            e.preventDefault(); erro.textContent = ''; botao.disabled = true;
            try {
                const r = await MomentusAPI.login({ email: document.getElementById('loginEmail').value.trim(), senha: document.getElementById('loginSenha').value });
                location.href = destino(r.usuario);
            } catch (ex) { erro.textContent = ex.message; }
            finally { botao.disabled = false; }
        });
    }

    const formCadastro = document.getElementById('formCadastro');
    if (formCadastro) {
        const erro = document.getElementById('erroCadastro');
        const botaoCadastro = formCadastro.querySelector('button[type="submit"]');
        const statusTermos = document.getElementById('statusTermosCadastro');
        const tentarNovamente = document.getElementById('recarregarTermosCadastro');
        const senhaInput = document.getElementById('cadastroSenha');
        const confirmacaoInput = document.getElementById('cadastroSenha2');
        async function carregarTermos() {
            botaoCadastro.disabled = true;
            tentarNovamente.hidden = true;
            statusTermos.textContent = 'Carregando a versão dos termos…';
            try {
                const info = await MomentusAPI.requisitar('/privacidade/info');
                if (!info.versao) throw new Error('Versão dos termos indisponível.');
                document.getElementById('versaoTermosCadastro').value = info.versao;
                statusTermos.textContent = 'Documentos disponíveis para leitura nos links acima.';
                botaoCadastro.disabled = false;
            } catch (_) {
                statusTermos.textContent = 'Não foi possível carregar os termos. Tente novamente; seus campos serão mantidos.';
                tentarNovamente.hidden = false;
            }
        }
        tentarNovamente.addEventListener('click', carregarTermos);
        carregarTermos();
        [senhaInput, confirmacaoInput].forEach(input => input.addEventListener('input', () => {
            confirmacaoInput.setCustomValidity('');
            confirmacaoInput.removeAttribute('aria-invalid');
        }));
        formCadastro.addEventListener('submit', async (e) => {
            e.preventDefault(); erro.textContent = '';
            if (formCadastro.getAttribute('aria-busy') === 'true') return;
            const senha = senhaInput.value;
            if (senha !== confirmacaoInput.value) {
                erro.textContent = 'As senhas não coincidem. Confira a confirmação da senha.';
                confirmacaoInput.setCustomValidity('As senhas não coincidem.');
                confirmacaoInput.setAttribute('aria-invalid', 'true');
                confirmacaoInput.focus();
                return;
            }
            if (!document.getElementById('versaoTermosCadastro').value) return;
            const payload = {
                nome: document.getElementById('cadastroNome').value.trim(),
                email: document.getElementById('cadastroEmail').value.trim(),
                telefone: document.getElementById('cadastroTelefone').value.trim(),
                senha,
                faixa_etaria: document.getElementById('cadastroFaixaEtaria').value,
                declaracao_idade: !!document.getElementById('cadastroFaixaEtaria').value,
                aceite_termos: document.getElementById('aceiteTermosCadastro').checked,
                versao_termos: document.getElementById('versaoTermosCadastro').value
            };
            const textoBotao = botaoCadastro.querySelector('span');
            const textoAnterior = textoBotao.textContent;
            botaoCadastro.disabled = true;
            textoBotao.textContent = 'Criando sua conta…';
            formCadastro.setAttribute('aria-busy', 'true');
            try { const r = await MomentusAPI.cadastro(payload); location.href = destino(r.usuario); }
            catch (ex) { erro.textContent = ex.message; erro.focus(); }
            finally { botaoCadastro.disabled = false; textoBotao.textContent = textoAnterior; formCadastro.removeAttribute('aria-busy'); }
        });
    }
})();
