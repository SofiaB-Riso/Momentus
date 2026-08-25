/* ================= LOCALIZAÇÃO COMPARTILHADA (catálogo / início) =================
   Guarda a localização (coordenadas ou cidade) que o usuário escolheu em QUALQUER
   página que busque fornecedores, para não pedir permissão de novo em outra página.
*/
const MomentusLocalizacao = (() => {
    const CHAVE = 'momentus_localizacao_fornecedores';
    const VALIDADE_MS = 1000 * 60 * 60 * 6; // 6 horas

    function salvar({ lat = null, lng = null, cidade = '' }) {
        try {
            localStorage.setItem(CHAVE, JSON.stringify({ lat, lng, cidade, quando: Date.now() }));
        } catch (_) { /* localStorage indisponível: ignora silenciosamente */ }
    }

    function carregar() {
        try {
            const bruto = localStorage.getItem(CHAVE);
            if (!bruto) return null;
            const dados = JSON.parse(bruto);
            if (!dados || (Date.now() - (dados.quando || 0)) > VALIDADE_MS) return null;
            const temAlgo = (dados.lat !== null && dados.lat !== undefined) || dados.cidade;
            return temAlgo ? dados : null;
        } catch (_) {
            return null;
        }
    }

    function limpar() {
        try { localStorage.removeItem(CHAVE); } catch (_) { /* ignora */ }
    }

    return { salvar, carregar, limpar };
})();
