/* O token fica apenas na memória da página; nunca no localStorage. */
(() => {
    window.addEventListener('hashchange', () => location.reload());
    const status = document.getElementById('statusRecuperacao');
    const recuperar = document.getElementById('formRecuperarSenha');
    const redefinir = document.getElementById('formRedefinirSenha');
    const token = new URLSearchParams(location.hash.slice(1)).get('token');
    const form = recuperar || redefinir;
    if (!form) return;
    const botao = form.querySelector('button[type="submit"]');
    function informar(mensagem, estado) {
        status.textContent = mensagem;
        status.dataset.estado = estado;
    }
    if (redefinir) {
        history.replaceState(null, '', location.pathname);
        if (!token) {
            informar('Este link não possui um token válido. Solicite outro e-mail pelo botão abaixo.', 'erro');
            botao.disabled = true;
            redefinir.hidden = true;
        }
    }
    let enviando = false;
    form.addEventListener('submit', async evento => {
        evento.preventDefault();
        if (enviando || (redefinir && !token)) return;
        const confirmacao = document.getElementById('confirmarNovaSenha');
        if (redefinir && document.getElementById('novaSenha').value !== confirmacao.value) {
            informar('As senhas não coincidem. Confira os dois campos.', 'erro');
            confirmacao.focus();
            return;
        }
        enviando = true;
        form.setAttribute('aria-busy', 'true');
        informar('Enviando sua solicitação…', 'carregando');
        botao.disabled = true;
        try {
            let resposta;
            if (recuperar) {
                resposta = await MomentusAPI.requisitar('/auth/recuperacao', {method: 'POST', body: JSON.stringify({email: document.getElementById('recuperarEmail').value.trim()})});
            } else {
                const senha = document.getElementById('novaSenha').value;
                resposta = await MomentusAPI.requisitar('/auth/redefinir-senha', {method: 'POST', body: JSON.stringify({token, senha})});
            }
            informar(resposta.mensagem, 'sucesso');
            if (redefinir) {
                redefinir.querySelectorAll('input').forEach(input => { input.value = ''; input.disabled = true; });
                redefinir.hidden = true;
                return;
            }
        } catch (erro) { informar(erro.message, 'erro'); }
        finally {
            enviando = false;
            form.setAttribute('aria-busy', 'false');
            if (!redefinir?.hidden) botao.disabled = false;
        }
    });
})();
