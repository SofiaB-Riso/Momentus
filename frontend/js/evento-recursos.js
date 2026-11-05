/* Casos de uso do evento: propostas, vagas e cronograma. Regras ficam na API. */
window.MomentusRecursos = (() => {
    const esc = MomentusUtils.escapeHTML;
    const moeda = v => Number(v).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
    const nomes = {equipe:'Equipe',montagem:'Montagem',transporte:'Transporte',limpeza:'Limpeza',materiais:'Materiais'};
    const estado = {filtros:{categoria:'buffet',teto:'',necessarios:[]},vagasEditando:false};

    function ajustarCampos(evento,container) {
        const limitar=container.querySelector('#limitarVagas'),numero=container.querySelector('#limiteVagas');
        if (!limitar || !numero) return;
        if (!estado.vagasEditando) {
            const limite=evento.planejamento?.limite_vagas;
            limitar.checked=limite!=null;numero.value=limite ?? Math.max(1,evento.convidados || 50);
        }
        numero.disabled=!limitar.checked;numero.required=limitar.checked;
        const titulo=container.querySelector('#tituloFormProposta');
        if(titulo)titulo.textContent=container.querySelector('#propostaEdicao')?.value ? 'Editar proposta' : 'Cadastrar proposta';
    }
    function ligar(evento,container) {
        const $=id=>container.querySelector('#'+id);
        const editar=evento.podeEditar!==false;
        const statusVagas=$('statusVagas'),fila=$('listaEsperaEvento');
        ajustarCampos(evento,container);
        $('limitarVagas').addEventListener('change',()=>{estado.vagasEditando=true;ajustarCampos(evento,container);});
        $('limiteVagas').addEventListener('input',()=>{estado.vagasEditando=true;});
        async function carregarFila() {
            try {
                const dados=await MomentusAPI.requisitar('/eventos/'+evento.id+'/lista-espera');
                if(!fila.isConnected)return;
                statusVagas.textContent=dados.limite_vagas==null
                    ? dados.confirmados+' presença(s) confirmada(s). Sem limite de vagas.'
                    : dados.confirmados+' de '+dados.limite_vagas+' vaga(s) confirmada(s); '+dados.fila.length+' na espera.';
                fila.innerHTML=dados.fila.map(p=>'<li><strong>'+esc(p.nome)+'</strong> · posição '+p.posicao+'</li>').join('');
            } catch(e){if(statusVagas.isConnected)statusVagas.textContent=e.message;}
        }
        carregarFila();
        MomentusUtils.protegerFormulario($('formVagas'),async()=>{
            try {
                const limite=$('limitarVagas').checked?Number($('limiteVagas').value):null;
                await MomentusAPI.requisitar('/eventos/'+evento.id+'/lista-espera',{method:'PUT',body:JSON.stringify({limite_vagas:limite})});
                estado.vagasEditando=false;
                await Momentus.sincronizarEventos();
                mostrarToast('Vagas atualizadas. A fila foi processada.');
            }catch(e){if(statusVagas.isConnected)statusVagas.textContent=e.message;else mostrarToast(e.message,'erro');}
        });
        const cronograma=$('gerarCronograma');
        cronograma.disabled=!editar;
        cronograma.textContent=evento.planejamento?.cronograma_ativo?'Regerar cronograma':'Gerar cronograma';
        $('statusCronograma').textContent=evento.planejamento?.cronograma_ativo
            ? 'Ativo. Ao gerar ou alterar a data, o horário ou o tipo, os prazos automáticos pendentes são distribuídos no período disponível. Concluídas e manuais são preservadas. Use Regerar para atualizar um cronograma antigo.' : '';
        cronograma.addEventListener('click',async()=>{
            cronograma.disabled=true;
            try {
                const dados=await MomentusAPI.requisitar('/eventos/'+evento.id+'/cronograma',{method:'POST'});
                await Momentus.sincronizarEventos();mostrarToast(dados.mensagem);
            }catch(e){mostrarToast(e.message,'erro');}finally{cronograma.disabled=!editar;}
        });

        const formFiltro=$('formCompararPropostas'),form=$('formProposta'),lista=$('listaComparacaoPropostas'),status=$('statusComparacao');
        const filtros=estado.filtros;
        $('categoriaComparacao').value=filtros.categoria;$('tetoComparacao').value=filtros.teto;
        formFiltro.querySelectorAll('[name=necessarios]').forEach(el=>{el.checked=filtros.necessarios.includes(el.value);});
        if(!editar){$('detalhesNovaProposta').hidden=true;$('novaProposta').hidden=true;}
        function limpar() {
            const atual=container.querySelector('#formProposta');if(!atual)return;
            atual.reset();atual.querySelector('#propostaEdicao').value='';
            $('tituloFormProposta').textContent='Cadastrar proposta';
            $('statusProposta').textContent='';
        }
        $('cancelarEdicaoProposta').addEventListener('click',limpar);
        $('novaProposta').addEventListener('click',()=>{limpar();$('detalhesNovaProposta').scrollIntoView({behavior:'smooth',block:'start'});$('nomeProposta').focus({preventScroll:true});});
        let consultaAtual = 0;
        async function comparar() {
            const consulta = ++consultaAtual;
            const query=new URLSearchParams({categoria:estado.filtros.categoria,teto:estado.filtros.teto,necessarios:estado.filtros.necessarios.join(',')});
            try {
                const dados=await MomentusAPI.requisitar('/eventos/'+evento.id+'/propostas/comparacao?'+query);
                if(!lista.isConnected || consulta !== consultaAtual)return;
                status.textContent=(dados.propostas.length ? dados.propostas.length+' proposta(s). ' : 'Nenhuma proposta nesta categoria. ')+
                    (dados.teto==null?'Sem teto definido. ':'Teto: '+moeda(dados.teto)+'. ')+dados.criterio;
                lista.innerHTML=dados.propostas.map(p=>'<article class="cardProposta '+(p.destaque?'propostaDestaque':'')+'" data-proposta="'+p.id+'">'+
                    (p.destaque?'<span class="seloProposta">Menor total entre as opções adequadas</span>':'')+
                    '<h3>'+esc(p.fornecedor)+'</h3><strong class="valorProposta">'+moeda(p.total)+'</strong>'+
                    '<p>Valor '+moeda(p.valor)+' − desconto '+moeda(p.desconto)+' + taxas '+moeda(p.taxas)+'</p>'+
                    '<p>'+p.parcelas+' parcela(s); primeira: '+moeda(p.primeira_parcela)+'</p>'+
                    '<p>Inclusos: '+esc(p.servicos.map(s=>nomes[s]).join(', ') || 'não informados')+'</p>'+
                    '<p>'+(p.dentro_orcamento?'Dentro do teto':'Acima do teto')+
                    (p.faltantes.length?' · Faltam: '+esc(p.faltantes.map(s=>nomes[s]).join(', ')):' · Atende aos serviços selecionados')+'</p>'+
                    (p.observacoes?'<p>'+esc(p.observacoes)+'</p>':'')+
                    (editar?'<div class="acoesProposta"><button type="button" class="botaoSecundario" data-editar-proposta="'+p.id+'">Editar</button><button type="button" class="botaoSecundario" data-remover-proposta="'+p.id+'">Remover</button></div>':'')+'</article>').join('');
                lista.querySelectorAll('[data-editar-proposta]').forEach(b=>b.addEventListener('click',()=>{
                    const p=dados.propostas.find(p=>String(p.id)===b.dataset.editarProposta);
                    $('propostaEdicao').value=p.id;$('nomeProposta').value=p.fornecedor;$('categoriaProposta').value=p.categoria;
                    for(const [campo,chave]of [['valorProposta','valor'],['descontoProposta','desconto'],['taxasProposta','taxas'],['parcelasProposta','parcelas'],['observacoesProposta','observacoes']])$(campo).value=p[chave];
                    form.querySelectorAll('[name=servicos]').forEach(el=>{el.checked=p.servicos.includes(el.value);});
                    $('tituloFormProposta').textContent='Editar proposta';
                    $('detalhesNovaProposta').scrollIntoView({behavior:'smooth',block:'start'});$('nomeProposta').focus({preventScroll:true});
                }));
                lista.querySelectorAll('[data-remover-proposta]').forEach(b=>b.addEventListener('click',async()=>{
                    if(!confirm('Remover esta proposta?'))return;b.disabled=true;
                    try{await MomentusAPI.requisitar('/eventos/'+evento.id+'/propostas/'+b.dataset.removerProposta,{method:'DELETE'});await Momentus.sincronizarEventos();}
                    catch(e){mostrarToast(e.message,'erro');b.disabled=false;}
                }));
            }catch(e){if(status.isConnected && consulta === consultaAtual)status.textContent=e.message;}
        }
        comparar();
        MomentusUtils.protegerFormulario(formFiltro,async()=>{
            estado.filtros={categoria:$('categoriaComparacao').value,teto:$('tetoComparacao').value,
                necessarios:[...formFiltro.querySelectorAll('[name=necessarios]:checked')].map(e=>e.value)};
            await comparar();
        });
        MomentusUtils.protegerFormulario(form,async()=>{
            const id=$('propostaEdicao').value;
            const dados={fornecedor:$('nomeProposta').value.trim(),categoria:$('categoriaProposta').value,
                valor:$('valorProposta').value,desconto:$('descontoProposta').value,taxas:$('taxasProposta').value,
                parcelas:Number($('parcelasProposta').value),observacoes:$('observacoesProposta').value.trim(),
                servicos:[...form.querySelectorAll('[name=servicos]:checked')].map(e=>e.value)};
            try {
                await MomentusAPI.requisitar('/eventos/'+evento.id+'/propostas'+(id?'/'+encodeURIComponent(id):''),{method:id?'PUT':'POST',body:JSON.stringify(dados)});
                estado.filtros.categoria=dados.categoria;limpar();
                await Momentus.sincronizarEventos();mostrarToast('Proposta salva para comparação.');
            }catch(e){const alvo=container.querySelector('#statusProposta');if(alvo)alvo.textContent=e.message;else mostrarToast(e.message,'erro');}
        });
    }
    return {ligar,ajustarCampos};
})();
