@extends('layouts.menu')

@section('titulo', $evento->nome_evento)

@section('sidebar')
    @include('layouts.partials.sidebar-evento', ['evento' => $evento, 'ativo' => 'evento'])
@endsection

@section('content')

    <header class="page-header">
        <div>
            <h1 class="page-header__titulo">{{ $evento->nome_evento }}</h1>
            <div class="page-header__subtitulo">{{ $evento->endereco_evento }}</div>
            <span class="badge-tipo">{{ $evento->tipo_evento }} &bull; {{ \Carbon\Carbon::parse($evento->data_evento)->format('d/m/Y') }}</span>
        </div>
        <div class="page-header__acoes">
            <details class="menu-kebab">
                <summary class="icone-botao" title="Mais opções">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="5" r="1.6" fill="currentColor"/><circle cx="12" cy="12" r="1.6" fill="currentColor"/><circle cx="12" cy="19" r="1.6" fill="currentColor"/></svg>
                </summary>
                <div class="menu-kebab__lista">
                    <a href="{{ route('eventos.edit', $evento) }}">Editar evento</a>
                    <form action="{{ route('eventos.destroy', $evento) }}" method="post" onsubmit="return confirm('Deseja realmente excluir este evento?');">
                        @csrf
                        @method('DELETE')
                        <button type="submit" class="is-perigo">Excluir evento</button>
                    </form>
                </div>
            </details>
        </div>
    </header>

    <section class="grid-cards">

        <article class="card">
            <div class="card__topo">
                <span class="card__titulo">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="9" cy="8" r="3" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 20c.6-3.3 2.9-5.2 5.5-5.2s4.9 1.9 5.5 5.2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="17" cy="9" r="2.4" stroke="currentColor" stroke-width="1.6"/><path d="M15.4 14.9c2 .3 3.7 1.9 4.1 4.6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                    Convidados
                </span>
                <a href="#" class="card__add"><svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></a>
            </div>
            <div class="card__vazio">
                <span>Nenhum convidado adicionado ainda</span>
            </div>
        </article>

        <article class="card">
            <div class="card__topo">
                <span class="card__titulo">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M4.5 12.5l4.5 4.5 10.5-11" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    Tarefas
                </span>
                <a href="#" class="card__add"><svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></a>
            </div>
            <div class="card__vazio">
                <span>Nenhuma tarefa criada ainda</span>
            </div>
        </article>

        <article class="card" id="orcamento">
            <div class="card__topo">
                <span class="card__titulo">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v10M9.5 9.5c0-1.1 1.1-2 2.5-2s2.5.7 2.5 1.8c0 2.4-5 1.2-5 3.6 0 1.1 1.1 1.8 2.5 1.8s2.5-.9 2.5-2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                    Orçamento
                </span>
                <a href="{{ route('eventos.edit', $evento) }}" class="card__add"><svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></a>
            </div>
            <div class="card__corpo">
                <div style="font-family:var(--fonte-titulo); font-size:26px; font-weight:600;">
                    R$ {{ number_format($evento->orcamento_evento, 2, ',', '.') }}
                </div>
                <div style="font-size:12.5px; color:var(--cor-texto-suave); margin-top:4px;">Orçamento total planejado</div>
            </div>
        </article>

        <article class="card card--planejamento" id="planejamento">
            <div class="card__topo">
                <span class="card__titulo">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M3 10h18M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                    Planejamento
                </span>
                <a href="#" class="card__add"><svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></a>
            </div>
            <div class="card__vazio">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/><path d="M12 7v5l3.5 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                <span>Aguardando criação do cronograma...</span>
            </div>
        </article>

        <article class="card">
            <div class="card__topo">
                <span class="card__titulo">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M6 10a6 6 0 1 1 12 0c0 3.2 1 5 2 6H4c1-1 2-2.8 2-6Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M10 19a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                    Notificações
                </span>
            </div>
            <div class="card__vazio">
                <span>Nenhuma notificação por aqui</span>
            </div>
        </article>

    </section>

@endsection
