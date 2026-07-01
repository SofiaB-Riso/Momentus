@extends('layouts.menu')

@section('titulo', 'Criar evento')

@section('sidebar')
    @include('layouts.partials.sidebar-dashboard', ['ativo' => 'planejar'])
@endsection

@section('content')

    <header class="page-header">
        <div>
            <h1 class="page-header__titulo">Criação de Evento</h1>
            <div class="page-header__subtitulo">Preencha os dados abaixo para planejar um novo momento</div>
        </div>
    </header>

    <div class="form-wrapper">
        <form method="post" action="{{ route('eventos.store') }}" class="form-card">
            @csrf

            <div class="form-grupo">
                <label for="nome_evento">Nome do evento</label>
                <input type="text" id="nome_evento" name="nome_evento" placeholder="Ex: Aniversário da Sofia" value="{{ old('nome_evento') }}">
            </div>

            <div class="form-linha">
                <div class="form-grupo">
                    <label for="tipo_evento">Tipo do evento</label>
                    <input type="text" id="tipo_evento" name="tipo_evento" placeholder="Ex: Aniversário, Casamento..." value="{{ old('tipo_evento') }}">
                </div>
                <div class="form-grupo">
                    <label for="data_evento">Data do evento</label>
                    <input type="date" id="data_evento" name="data_evento" value="{{ old('data_evento') }}">
                </div>
            </div>

            <div class="form-grupo">
                <label for="endereco_evento">Endereço do evento</label>
                <input type="text" id="endereco_evento" name="endereco_evento" placeholder="Rua, número, bairro, cidade" value="{{ old('endereco_evento') }}">
            </div>

            <div class="form-grupo">
                <label for="orcamento_evento">Orçamento do evento (R$)</label>
                <input type="number" step="0.01" min="0" id="orcamento_evento" name="orcamento_evento" placeholder="0,00" value="{{ old('orcamento_evento') }}">
            </div>

            <div class="form-acoes">
                <button type="submit" class="botao botao--primario">Criar Evento</button>
                <a href="{{ route('eventos.index') }}" class="botao botao--secundario">Cancelar</a>
            </div>
        </form>
    </div>

@endsection
