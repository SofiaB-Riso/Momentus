/* Controle compartilhado por login, cadastro e redefinição de senha. */
(() => {
    const icones = `
        <svg data-olho-aberto viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>
        <svg data-olho-fechado viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" hidden><path d="m3 3 18 18M10.6 5.1 12 5c6.5 0 10 7 10 7a18.5 18.5 0 0 1-3 3.9M6.1 6.1A21 21 0 0 0 2 12s3.5 7 10 7a12.6 12.6 0 0 0 5.9-1.5M9.9 9.9a3 3 0 0 0 4.2 4.2"/></svg>`;

    document.querySelectorAll('[data-mostrar-senha]').forEach(botao => {
        const input = document.getElementById(botao.dataset.mostrarSenha);
        if (!input) return;
        botao.innerHTML = icones;
        botao.addEventListener('click', () => {
            const visivel = input.type === 'password';
            input.type = visivel ? 'text' : 'password';
            const rotulo = visivel ? 'Ocultar senha' : 'Mostrar senha';
            botao.setAttribute('aria-pressed', String(visivel));
            botao.setAttribute('aria-label', rotulo);
            botao.title = rotulo;
            botao.querySelector('[data-olho-aberto]').toggleAttribute('hidden', visivel);
            botao.querySelector('[data-olho-fechado]').toggleAttribute('hidden', !visivel);
        });
    });
})();
