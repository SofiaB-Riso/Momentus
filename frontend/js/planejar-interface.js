/* Prévia e navegação visual; salvamento e regras continuam em script.js/API. */
(function () {
    const form = document.getElementById('formPlanejar');
    if (!form) return;
    const tipos = {
        aniversario:'<path d="M4 12h16v9H4zM4 16c2 2 4-2 6 0s4-2 6 0 2 1 4 0M7 12V8M12 12V8M17 12V8M7 4v1M12 3v2M17 4v1"/>',
        casamento:'<circle cx="8" cy="14" r="5"/><circle cx="16" cy="14" r="5"/><path d="m6 6 2-3 2 3-2 3-2-3Zm8 0 2-3 2 3-2 3-2-3Z"/>',
        churrasco:'<path d="M12 3c2 5-2 5 1 8 1-1 2-2 2-4 5 5 6 12-1 14-6 2-12-4-9-9 1 3 2 3 3 3-1-5 2-7 4-12Z"/>',
        formatura:'<path d="m2 9 10-5 10 5-10 5L2 9ZM6 11v6c4 3 8 3 12 0v-6M22 9v8"/>',
        corporativo:'<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1M10 21v-3h4v3"/>',
        chadebebe:'<path d="M3 11h17a8 8 0 0 1-16 0M12 11V3a8 8 0 0 1 8 8M2 6h2l2 5"/><circle cx="7" cy="21" r="1"/><circle cx="17" cy="21" r="1"/>',
        noivado:'<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/>',
        batizado:'<path d="M12 3c3 4 7 8 7 12a7 7 0 0 1-14 0c0-4 4-8 7-12ZM8 15a4 4 0 0 0 4 4"/>',
        confraternizacao:'<path d="M3 3h6l1 7a4 4 0 0 1-8 0l1-7ZM15 3h6l1 7a4 4 0 0 1-8 0l1-7ZM6 14v7M18 14v7M3 21h6M15 21h6M3 8h6M15 8h6"/>',
        outro:'<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5L12 3Z"/>'
    };
    document.querySelectorAll('.chipCategoria').forEach(chip => {
        const marca = chip.querySelector('.emoji');
        marca.setAttribute('aria-hidden', 'true');
        marca.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">' + tipos[chip.dataset.tipo] + '</svg>';
    });
    function sincronizarPrevia() {
        const nome = document.getElementById('nomeEvento').value.trim();
        const resumoNome = document.getElementById('resumoNome');
        const resumoHorario = document.getElementById('resumoHorario');
        const horario = document.getElementById('horaEvento').value || 'A definir';
        if (resumoNome.textContent !== (nome || 'Seu próximo momento')) resumoNome.textContent = nome || 'Seu próximo momento';
        if (resumoHorario.textContent !== horario) resumoHorario.textContent = horario;
    }
    let quadro;
    function agendarPrevia() {
        cancelAnimationFrame(quadro);
        quadro = requestAnimationFrame(sincronizarPrevia);
    }
    ['nomeEvento', 'horaEvento'].forEach(id => {
        document.getElementById(id).addEventListener('input', agendarPrevia);
        document.getElementById(id).addEventListener('change', agendarPrevia);
    });
    document.addEventListener('momentus:idioma-alterado', agendarPrevia);
    const carregamento = new MutationObserver(() => {
        if (form.getAttribute('aria-busy') === 'false') { sincronizarPrevia(); carregamento.disconnect(); }
    });
    carregamento.observe(form, {attributes:true, attributeFilter:['aria-busy']});
    sincronizarPrevia();

    const links = [...document.querySelectorAll('.etapasPlanejamento a')];
    function selecionar(id) {
        links.forEach(link => {
            if (link.hash === '#' + id) link.setAttribute('aria-current', 'step');
            else link.removeAttribute('aria-current');
        });
    }
    links.forEach(link => link.addEventListener('click', () => selecionar(link.hash.slice(1))));
    const secoes = new IntersectionObserver(entries => {
        const atual = entries.find(entry => entry.isIntersecting);
        if (atual) selecionar(atual.target.id);
    }, {rootMargin:'-20% 0px -60% 0px'});
    document.querySelectorAll('.secaoPlanejamento').forEach(secao => secoes.observe(secao));
})();
