/* Seletor de horário: relógio de 24 horas e minutos exatos, sem dependências. */
(() => {
    const campo = document.getElementById('horaEvento');
    const dialog = document.getElementById('dialogHorario');
    if (!campo || !dialog) return;
    const abrir = document.getElementById('abrirRelogio');
    const horas = document.getElementById('relogioHoras');
    const minutos = document.getElementById('relogioMinutos');
    const numeros = document.getElementById('numerosRelogio');
    const modoHoras = document.getElementById('modoHoras');
    const modoMinutos = document.getElementById('modoMinutos');
    const ponteiro = dialog.querySelector('.ponteiroRelogio');
    let modo = 'horas';
    const doisDigitos = (valor) => String(valor).padStart(2, '0');

    for (const [seletor, total] of [[horas, 24], [minutos, 60]]) {
        for (let n = 0; n < total; n++) seletor.add(new Option(doisDigitos(n), n));
    }

    function renderizar() {
        const selecionandoHoras = modo === 'horas';
        modoHoras.setAttribute('aria-pressed', String(selecionandoHoras));
        modoMinutos.setAttribute('aria-pressed', String(!selecionandoHoras));
        const valor = Number(selecionandoHoras ? horas.value : minutos.value);
        const angulo = selecionandoHoras ? valor % 12 * 30 : valor * 6;
        const raio = selecionandoHoras && (valor === 0 || valor > 12) ? 29 : 41;
        ponteiro.style.transform = `rotate(${angulo}deg)`;
        ponteiro.style.height = `${raio}%`;
        numeros.replaceChildren();
        const valores = selecionandoHoras ? Array.from({ length: 24 }, (_, i) => i) : Array.from({ length: 12 }, (_, i) => i * 5);
        for (const n of valores) {
            const graus = selecionandoHoras ? n % 12 * 30 : n * 6;
            const distancia = selecionandoHoras && (n === 0 || n > 12) ? 29 : 41;
            const radianos = graus * Math.PI / 180;
            const botao = document.createElement('button');
            botao.type = 'button';
            botao.className = 'numeroRelogio';
            botao.textContent = doisDigitos(n);
            botao.setAttribute('aria-label', `${Momentus.t(selecionandoHoras ? 'relogioHoras' : 'relogioMinutos')}: ${doisDigitos(n)}`);
            botao.setAttribute('aria-pressed', String(n === valor));
            botao.style.left = `${50 + Math.sin(radianos) * distancia}%`;
            botao.style.top = `${50 - Math.cos(radianos) * distancia}%`;
            botao.addEventListener('click', () => {
                if (selecionandoHoras) {
                    horas.value = String(n);
                    modo = 'minutos';
                    renderizar();
                    modoMinutos.focus();
                } else {
                    minutos.value = String(n);
                    renderizar();
                    numeros.querySelector('[aria-pressed="true"]')?.focus();
                }
            });
            numeros.appendChild(botao);
        }
    }

    function abrirRelogio() {
        if (dialog.open) return;
        const atual = /^([01]\d|2[0-3]):([0-5]\d)$/.exec(campo.value);
        const agora = new Date();
        horas.value = String(atual ? Number(atual[1]) : agora.getHours());
        minutos.value = String(atual ? Number(atual[2]) : agora.getMinutes());
        modo = 'horas';
        renderizar();
        dialog.showModal();
        horas.focus();
    }

    function aplicar(valor) {
        campo.value = valor;
        campo.dispatchEvent(new Event('input', { bubbles: true }));
        campo.dispatchEvent(new Event('change', { bubbles: true }));
        dialog.close();
    }

    abrir.addEventListener('click', abrirRelogio);
    campo.addEventListener('click', (e) => { e.preventDefault(); abrirRelogio(); });
    horas.addEventListener('change', () => { modo = 'horas'; renderizar(); });
    minutos.addEventListener('change', () => { modo = 'minutos'; renderizar(); });
    modoHoras.addEventListener('click', () => { modo = 'horas'; renderizar(); });
    modoMinutos.addEventListener('click', () => { modo = 'minutos'; renderizar(); });
    document.getElementById('confirmarHorario').addEventListener('click', () => {
        aplicar(`${doisDigitos(horas.value)}:${doisDigitos(minutos.value)}`);
    });
    document.getElementById('limparHorario').addEventListener('click', () => aplicar(''));
    dialog.querySelector('.fecharRelogio').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (e) => {
        if (e.target !== dialog) return;
        const r = dialog.getBoundingClientRect();
        if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close();
    });
    document.addEventListener('momentus:idioma-alterado', () => { if (dialog.open) renderizar(); });
})();
