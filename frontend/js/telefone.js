const MomentusTelefone = (() => {
    function limpar(valor) {
        const texto = String(valor || '');
        // Um e-mail sugerido pelo navegador não deve virar um telefone com os
        // algarismos do endereço (por exemplo, pessoa13@... não significa 13).
        if (texto.includes('@')) return '';
        return texto.replace(/[^0-9+]/g, '').replace(/(?!^)\+/g, '');
    }

    function atualizar(campo) {
        const valor = campo.value;
        const limpo = limpar(valor);
        if (valor === limpo) return;
        const inicio = campo.selectionStart;
        const fim = campo.selectionEnd;
        campo.value = limpo;
        if (inicio !== null && fim !== null) {
            campo.setSelectionRange(limpar(valor.slice(0, inicio)).length, limpar(valor.slice(0, fim)).length);
        }
    }

    const campos = [...document.querySelectorAll('input[type="tel"]')];
    campos.forEach(campo => {
        atualizar(campo);
        // Alguns gerenciadores preenchem o telefone ao interagir com a senha;
        // observe o formulário para também corrigir esse preenchimento tardio.
        const origem = campo.form || campo;
        ['input', 'change', 'focusin'].forEach(evento => {
            origem.addEventListener(evento, () => atualizar(campo));
        });
    });
    window.addEventListener('pageshow', () => campos.forEach(atualizar));

    return { limpar };
})();
