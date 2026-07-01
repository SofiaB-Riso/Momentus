@extends('layouts.menu')

@section('titulo', 'Início')

@section('sidebar')
    @include('layouts.partials.sidebar-dashboard', ['ativo' => 'inicio'])
@endsection

@section('content')

    @php
        $hoje = \Carbon\Carbon::now();
        $inicioMes = $hoje->copy()->startOfMonth();
        $fimMes = $hoje->copy()->endOfMonth();
        $diaSemanaInicio = $inicioMes->dayOfWeek; // 0 = domingo

        $celulas = [];
        for ($i = 0; $i < $diaSemanaInicio; $i++) {
            $celulas[] = null;
        }
        for ($d = 1; $d <= $fimMes->day; $d++) {
            $celulas[] = $d;
        }
        while (count($celulas) % 7 !== 0) {
            $celulas[] = null;
        }

        $diasComEvento = $eventos
            ->map(fn($e) => \Carbon\Carbon::parse($e->data_evento))
            ->filter(fn($data) => $data->between($inicioMes, $fimMes))
            ->map(fn($data) => $data->day)
            ->toArray();

        $proximosEventos = collect($eventos)
            ->map(fn($e) => ['evento' => $e, 'data' => \Carbon\Carbon::parse($e->data_evento)])
            ->sortBy('data')
            ->take(2)
            ->values();

        $meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
    @endphp

    <header class="page-header">
        <div>
            <h1 class="page-header__titulo">Olá, nome usuário!</h1>
        </div>
        <div class="page-header__acoes">
            <button class="icone-botao" title="Notificações">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M6 10a6 6 0 1 1 12 0c0 3.2 1 5 2 6H4c1-1 2-2.8 2-6Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M10 19a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
            </button>
            <details class="menu-kebab">
                <summary class="icone-botao" title="Mais opções">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="5" r="1.6" fill="currentColor"/><circle cx="12" cy="12" r="1.6" fill="currentColor"/><circle cx="12" cy="19" r="1.6" fill="currentColor"/></svg>
                </summary>
                <div class="menu-kebab__lista">
                    <a href="{{ route('eventos.create') }}">Planejar novo evento</a>
                </div>
            </details>
        </div>
    </header>

    <section class="grid-cards">
        @forelse ($eventos as $evento)
            <article class="card card--evento">
                <div class="card-evento">
                    <div class="card-evento__topo">
                        <span class="card-evento__nome">{{ $evento->nome_evento }}</span>
                        <a href="{{ route('eventos.show', $evento) }}" class="card-evento__seta" title="Ver evento">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        </a>
                    </div>
                    <div class="card-evento__info">
                        {{ $evento->endereco_evento }}<br>
                        {{ \Carbon\Carbon::parse($evento->data_evento)->format('d/m') }} &bull; {{ $evento->tipo_evento }}
                    </div>
                    <div class="card-evento__rodape">
                        Última alteração: {{ optional($evento->updated_at)->format('d/m/y \à\s H:i') ?? '—' }}
                    </div>
                </div>
            </article>
        @empty
        @endforelse

        <a href="{{ route('eventos.create') }}" class="card card--tracejado">
            <div class="card-planejar" style="width:100%">
                <span>Planejar evento</span>
                <span class="card__add">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
                </span>
            </div>
        </a>
    </section>

    <div class="regua"></div>

    <section class="grid-secundaria">

        <div class="painel">
            <h2 class="painel__titulo">Calendário</h2>

            <div class="calendario__nav">
                <button class="calendario__nav-botao" type="button" disabled>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M15 6l-6 6 6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </button>
                <span class="calendario__seletor">{{ $meses[$hoje->month - 1] }} &nbsp; {{ $hoje->year }}</span>
                <button class="calendario__nav-botao" type="button" disabled>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </button>
            </div>

            <div class="calendario__layout">
                <table class="calendario__grade">
                    <thead>
                        <tr>
                            <th>Do</th><th>Se</th><th>Te</th><th>Qu</th><th>Qu</th><th>Se</th><th>Sa</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach (array_chunk($celulas, 7) as $semana)
                            <tr>
                                @foreach ($semana as $dia)
                                    <td>
                                        @if ($dia)
                                            <span class="calendario__dia
                                                {{ $dia === $hoje->day ? 'is-selecionado' : '' }}
                                                {{ in_array($dia, $diasComEvento) && $dia !== $hoje->day ? 'is-evento' : '' }}">
                                                {{ $dia }}
                                            </span>
                                        @endif
                                    </td>
                                @endforeach
                            </tr>
                        @endforeach
                    </tbody>
                </table>

                <div class="calendario__eventos">
                    @forelse ($proximosEventos as $index => $item)
                        <div class="calendario__evento-pill {{ $index % 2 === 0 ? 'calendario__evento-pill--roxo' : 'calendario__evento-pill--rosa' }}">
                            <span class="calendario__evento-data">{{ $item['data']->format('d') }} {{ $meses[$item['data']->month - 1] }}</span>
                            <span>{{ $item['evento']->tipo_evento }}</span>
                        </div>
                    @empty
                        <div class="calendario__evento-vazio"></div>
                        <div class="calendario__evento-vazio"></div>
                    @endforelse
                </div>
            </div>
        </div>

        <div class="painel">
            <div class="pesquisa__campo">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"/><path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
                <input type="text" placeholder="Pesquisar . . ." disabled>
            </div>

            <div class="produto-lista">
                <div class="produto-card">
                    <div class="produto-card__thumb"></div>
                    <div>
                        <div class="produto-card__nome">Salgadinhos da Jane</div>
                        <div class="produto-card__categoria">Salgados para eventos</div>
                        <div class="produto-card__estrelas">
                            @for ($i = 0; $i < 5; $i++)
                                <svg class="{{ $i < 2 ? '' : 'is-vazia' }}" width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3 6.5 7 .9-5.2 4.9 1.4 6.9L12 17.9 5.8 21.2l1.4-6.9L2 9.4l7-.9L12 2Z"/></svg>
                            @endfor
                        </div>
                    </div>
                </div>
                <div class="produto-card">
                    <div class="produto-card__thumb"></div>
                    <div>
                        <div class="produto-card__nome">Boquinha</div>
                        <div class="produto-card__categoria">Salgadinhos de festa</div>
                        <div class="produto-card__estrelas">
                            @for ($i = 0; $i < 5; $i++)
                                <svg class="{{ $i < 3 ? '' : 'is-vazia' }}" width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3 6.5 7 .9-5.2 4.9 1.4 6.9L12 17.9 5.8 21.2l1.4-6.9L2 9.4l7-.9L12 2Z"/></svg>
                            @endfor
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </section>

@endsection
