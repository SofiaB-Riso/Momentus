/* Extensões da página do evento: usa os mesmos formulários, cartões e temas. */
window.MomentusPlanejamento = (() => {
    const esc = MomentusUtils.escapeHTML;
    const moeda = (v) => Number(v || 0).toLocaleString('pt-BR', {style:'currency', currency:'BRL'});
    const estado = { fornecedores: null, filtros: null, categoria: 'buffet' };
    const acoes = {
        evento_criado:'Evento criado', evento_atualizado:'Detalhes atualizados', convidado_adicionado:'Convidado adicionado',
        convidado_atualizado:'Convidado atualizado', convidado_removido:'Convidado removido', rsvp_atualizado:'Resposta ao convite',
        colaborador_convidado:'Convite de colaboração', colaborador_respondeu:'Resposta à colaboração',
        colaborador_atualizado:'Permissão ou participação atualizada', colaborador_removido:'Colaborador removido',
        item_assumido:'Item reservado', item_liberado:'Item liberado', item_compartilhado_adicionado:'Item compartilhado adicionado',
        item_compartilhado_atualizado:'Item compartilhado atualizado', item_compartilhado_removido:'Item compartilhado removido',
        item_catalogo_adicionado:'Item do catálogo adicionado', item_catalogo_atualizado:'Quantidade atualizada', item_catalogo_removido:'Item do catálogo removido',
        despesa_adicionada:'Despesa registrada', despesa_removida:'Despesa removida', comprovante_enviado:'Comprovante enviado',
        rateio_atualizado:'Rateio atualizado', tarefa_adicionada:'Tarefa criada', tarefa_atualizada:'Tarefa atualizada', tarefa_removida:'Tarefa removida',
        foto_adicionada:'Foto enviada', foto_removida:'Foto removida', local_adicionado:'Espaço salvo', local_removido:'Espaço removido'
    };

    function mapasHTML(mapas) {
        if (!mapas?.google) return '<span class="textoAuxiliarPainel">Defina o endereço do evento para abrir a rota.</span>';
        return `<a class="botaoSecundario" href="${esc(mapas.google)}" target="_blank" rel="noopener">Google Maps ↗</a>
            <a class="botaoSecundario" href="${esc(mapas.waze)}" target="_blank" rel="noopener">Waze ↗</a>`;
    }

    function ligar(evento, container) {
        const $ = id => container.querySelector('#' + id);
        const editar = evento.podeEditar !== false;
        $('mapasEvento').innerHTML = mapasHTML(evento.mapas);
        $('atualizacaoEvento').textContent = 'Atualização automática ativa';
        const historicoAba = container.querySelector('[data-aba="historico"]');
        historicoAba.hidden = evento.permissao !== 'dono';
        if (evento.permissao === 'dono') {
            const destino = $('historicoEvento');
            MomentusAPI.requisitar(`/eventos/${evento.id}/logs`).then(logs => {
                if (!destino.isConnected) return;
                destino.innerHTML = logs.length ? logs.map(l => `<li class="registroHistorico"><span class="pontoHistorico" aria-hidden="true"></span><div>
                    <strong>${esc(acoes[l.acao] || l.acao.replaceAll('_', ' '))}</strong><p>${esc(l.detalhe)}</p>
                    <small>${esc(l.autor)} · ${esc(new Date(l.criado_em + (l.criado_em.endsWith('Z') ? '' : 'Z')).toLocaleString('pt-BR'))}</small>
                    </div></li>`).join('') : '<li class="textoAuxiliarPainel">O histórico aparecerá aqui conforme o evento for organizado.</li>';
            }).catch(e => { if (destino.isConnected) destino.textContent = e.message; });
        }

        const filtros = $('formBuscaLocais');
        const valores = estado.filtros || { cidade: evento.cidade, orcamento: evento.orcamento || '', capacidade: Math.max(evento.convidados, evento.confirmados, 1), estilo: evento.estilo };
        Object.entries(valores).forEach(([k,v]) => { if (filtros.elements[k]) filtros.elements[k].value = v; });
        const msg = $('mensagemDescoberta');
        async function buscarLocais() {
            estado.filtros = Object.fromEntries(new FormData(filtros));
            const lista = $('locaisCompativeis');
            const query = new URLSearchParams(estado.filtros);
            try {
                const dados = await MomentusAPI.requisitar(`/eventos/${evento.id}/locais?${query}`);
                if (!lista.isConnected) return;
                $('contagemLocais').textContent = `${dados.locais.length} compatível(is) · ${dados.total_salvos} salvo(s)`;
                lista.innerHTML = dados.locais.length ? dados.locais.map(l => `<article class="cartaoDescoberta">
                    <span class="tagCard">${esc(l.estilo)}</span><h3>${esc(l.nome)}</h3><p>${esc(l.endereco)} · ${esc(l.cidade)}</p>
                    <div class="chipsSugestao"><span>Até ${l.capacidade} pessoas</span><span>${moeda(l.preco)} de locação</span></div>
                    <div class="acoesDescoberta">${mapasHTML(l.mapas)}${editar ? `<button type="button" class="botaoPrimario" data-usar-local="${l.id}">Usar endereço</button>` : ''}</div>
                    </article>`).join('') : '<p class="estadoVazioClaro">Nenhum espaço salvo atende a estes filtros. Ajuste a busca ou registre uma opção com o orçamento confirmado.</p>';
                lista.querySelectorAll('[data-usar-local]').forEach(b => b.addEventListener('click', async () => {
                    const local = dados.locais.find(l => String(l.id) === b.dataset.usarLocal);
                    b.disabled = true;
                    try {
                        await MomentusAPI.atualizarEvento(evento.id, {endereco_evento: local.endereco, cidade_evento: local.cidade});
                        await Momentus.sincronizarEventos();
                        mostrarToast('Endereço atualizado. Os convidados verão o aviso no convite.');
                    } catch (e) { msg.textContent = e.message; } finally { b.disabled = false; }
                }));
            } catch(e) { if (lista.isConnected) lista.textContent = e.message; }
        }
        filtros.addEventListener('submit', e => { e.preventDefault(); buscarLocais(); });
        buscarLocais();

        const formLocal = $('formSalvarLocal');
        formLocal.elements.cidade.value = evento.cidade || '';
        formLocal.elements.estilo.value = evento.estilo || '';
        formLocal.addEventListener('submit', async e => {
            e.preventDefault(); msg.textContent = ''; e.submitter.disabled = true;
            try {
                await MomentusAPI.requisitar(`/eventos/${evento.id}/locais`, {method:'POST', body:JSON.stringify(Object.fromEntries(new FormData(formLocal)))});
                formLocal.reset();
                await Momentus.sincronizarEventos();
                mostrarToast('Espaço salvo para comparar com os critérios do evento.');
            } catch(e) { msg.textContent = e.message; } finally { e.submitter.disabled = false; }
        });
        const salvos = $('todosLocaisSalvos');
        salvos.innerHTML = (evento.locais || []).map(l => `<div class="linhaItemEvento"><div class="infoItemEvento"><strong>${esc(l.nome)}</strong><p class="metaItemEvento">${esc(l.cidade)} · ${l.capacidade} pessoas · ${moeda(l.preco)}</p></div>
            ${editar ? `<button type="button" class="botaoRemoverConvidado" data-remover-local="${l.id}" aria-label="Remover ${esc(l.nome)}">×</button>` : ''}</div>`).join('') || '<p class="textoAuxiliarPainel">Você ainda não salvou espaços.</p>';
        salvos.querySelectorAll('[data-remover-local]').forEach(b => b.addEventListener('click', async () => {
            b.disabled = true;
            try { await MomentusAPI.requisitar(`/eventos/${evento.id}/locais/${b.dataset.removerLocal}`, {method:'DELETE'}); await Momentus.sincronizarEventos(); }
            catch(e) { msg.textContent = e.message; } finally { b.disabled = false; }
        }));

        const formBusca = $('formFornecedoresEvento');
        formBusca.elements.categoria.value = estado.categoria;
        formBusca.elements.cidade.value = evento.cidade || '';
        function mostrarFornecedores(dados) {
            const lista = $('fornecedoresEvento');
            $('avisoFornecedores').textContent = [dados.aviso, dados.observacao].filter(Boolean).join(' ');
            lista.innerHTML = dados.resultados.length ? dados.resultados.map((f, indice) => `<article class="cartaoDescoberta">
                <span class="tagCard">${f.fonte === 'google' ? 'Google Maps' : 'Catálogo Momentus'}</span>
                <h3>${esc(f.nome_empresa)}</h3><p>${esc(f.endereco || f.cidade)}</p>
                <p class="notaFornecedor">${f.avaliacao != null ? `★ ${Number(f.avaliacao).toFixed(1)}${f.total_avaliacoes ? ` · ${f.total_avaliacoes} avaliações` : ''}` : 'Sem avaliações disponíveis'}</p>
                <small>${esc(f.motivo)}</small><div class="acoesDescoberta">${mapasHTML(f.mapas)}
                ${estado.categoria === 'espacos' && editar ? `<button type="button" class="botaoPrimario" data-preencher-local="${indice}">Comparar orçamento</button>` : ''}</div></article>`).join('') : '<p class="estadoVazioClaro">Nenhuma sugestão encontrada para esta busca.</p>';
            lista.querySelectorAll('[data-preencher-local]').forEach(b => b.addEventListener('click', () => {
                const f = dados.resultados[Number(b.dataset.preencherLocal)];
                formLocal.elements.nome.value = f.nome_empresa;
                formLocal.elements.endereco.value = f.endereco || '';
                formLocal.elements.cidade.value = dados.cidade || evento.cidade || '';
                $('cadastroEspaco').open = true;
                formLocal.scrollIntoView({behavior:'smooth', block:'center'});
                formLocal.elements.capacidade.focus({preventScroll:true});
            }));
        }
        if (estado.fornecedores) mostrarFornecedores(estado.fornecedores);
        formBusca.addEventListener('submit', async e => {
            e.preventDefault(); e.submitter.disabled = true;
            estado.categoria = formBusca.elements.categoria.value;
            const aviso = $('avisoFornecedores'); aviso.textContent = 'Buscando opções para o seu evento...';
            try {
                const query = new URLSearchParams(new FormData(formBusca));
                const dados = await MomentusAPI.requisitar(`/eventos/${evento.id}/recomendacoes?${query}`);
                estado.fornecedores = dados;
                if (formBusca.isConnected) mostrarFornecedores(dados);
            } catch(e) { if (aviso.isConnected) aviso.textContent = e.message; }
            finally { e.submitter.disabled = false; }
        });
    }
    return {ligar};
})();
