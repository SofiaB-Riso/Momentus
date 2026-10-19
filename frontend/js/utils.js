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

    return { escapeHTML, estrelas, formatarDataBR, dataPorExtenso };
})();
