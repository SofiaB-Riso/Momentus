(function () {
    const params = new URLSearchParams(location.search);

    function destino(usuario) {
        const proximo = params.get('next');
        if (proximo && !proximo.startsWith('http')) return proximo;
        return 'inicio.html';
    }

    MomentusAPI.me().then((r) => {
        if (r && r.usuario) location.href = destino(r.usuario);
    }).catch(() => {});

    const formLogin = document.getElementById('formLogin');
    if (formLogin) {
        const erro = document.getElementById('erroLogin');
        const botao = formLogin.querySelector('button[type="submit"]');
        document.getElementById('mostrarSenhaLogin').addEventListener('change', (e) => {
            document.getElementById('loginSenha').type = e.target.checked ? 'text' : 'password';
        });
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
        formCadastro.addEventListener('submit', async (e) => {
            e.preventDefault();
            const erro = document.getElementById('erroCadastro'); erro.textContent = '';
            const senha = document.getElementById('cadastroSenha').value;
            if (senha !== document.getElementById('cadastroSenha2').value) { erro.textContent = 'As senhas não coincidem.'; return; }
            const payload = {
                nome: document.getElementById('cadastroNome').value.trim(),
                email: document.getElementById('cadastroEmail').value.trim(),
                telefone: document.getElementById('cadastroTelefone').value.trim(),
                senha
            };
            const botao = e.submitter; botao.disabled = true;
            try { const r = await MomentusAPI.cadastro(payload); location.href = destino(r.usuario); }
            catch (ex) { erro.textContent = ex.message; }
            finally { botao.disabled = false; }
        });
    }
})();
