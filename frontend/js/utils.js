/* Funções de apresentação compartilhadas pelas páginas, sem estado de sessão. */
const MomentusUtils = (() => {
    function escapeHTML(valor) {
        const div = document.createElement('div');
        div.textContent = String(valor ?? '');
        return div.innerHTML.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    function estrelas(nota) {
        const quantidade = Math.max(0, Math.min(5, Math.round(Number(nota) || 0)));
        return '★'.repeat(quantidade) + '<span class="apagada">' + '★'.repeat(5 - quantidade) + '</span>';
    }

    function formatarDataBR(valorISO) {
        if (!valorISO) return '—';
        const [ano, mes, dia] = valorISO.split('-');
        return `${dia}/${mes}/${ano}`;
    }

    function dataPorExtenso(valorISO) {
        return valorISO ? new Date(valorISO + 'T12:00:00').toLocaleDateString('pt-BR', {
            day: '2-digit', month: 'long', year: 'numeric'
        }) : '—';
    }

    function tempoDecorrido(instante, agora = Date.now(), idioma = 'pt') {
        if (!instante) return null;
        const data = new Date(instante).getTime();
        if (!Number.isFinite(data) || data > agora + 60000) return null;
        const segundos = Math.max(0, (agora - data) / 1000);
        if (segundos < 3600) return { recente: true, relativo: '' };
        const [duracao, unidade] = segundos >= 31536000 ? [31536000, 'year']
            : segundos >= 2592000 ? [2592000, 'month']
            : segundos >= 86400 ? [86400, 'day'] : [3600, 'hour'];
        const locale = {pt:'pt-BR', en:'en-US', es:'es-ES'}[idioma] || 'pt-BR';
        return { recente: false, relativo: new Intl.RelativeTimeFormat(locale, {numeric:'always'}).format(-Math.floor(segundos / duracao), unidade) };
    }

    const enviosPendentes = new Set();
    function protegerFormulario(form, acao) {
        const chave = form.id || form;
        form.querySelectorAll('button[type="submit"]').forEach(b=>{b.disabled=enviosPendentes.has(chave);});
        form.addEventListener('submit', async evento => {
            evento.preventDefault();
            if (enviosPendentes.has(chave)) return;
            enviosPendentes.add(chave);
            form.querySelectorAll('button[type="submit"]').forEach(b=>{b.disabled=true;});
            try {await acao(evento);}
            catch (erro) {if (typeof window.mostrarToast === 'function')window.mostrarToast('Não foi possível concluir o envio. Tente novamente.','erro');console.error(erro);}
            finally {
                enviosPendentes.delete(chave);
                const atual=form.id ? document.getElementById(form.id) : form;
                atual?.querySelectorAll('button[type="submit"]').forEach(b=>{b.disabled=false;});
            }
        });
    }

    function chaveEnvio() {
        const bytes=crypto.getRandomValues(new Uint8Array(16));
        bytes[6]=(bytes[6]&15)|64;bytes[8]=(bytes[8]&63)|128;
        const texto=[...bytes].map(b=>b.toString(16).padStart(2,'0')).join('');
        return `${texto.slice(0,8)}-${texto.slice(8,12)}-${texto.slice(12,16)}-${texto.slice(16,20)}-${texto.slice(20)}`;
    }

    return { escapeHTML, estrelas, formatarDataBR, dataPorExtenso, tempoDecorrido, protegerFormulario, chaveEnvio };
})();
