@extends('layouts.menu')

@section('titulo', 'Editar ' . $evento->nome_evento)

@section('sidebar')
    @include('layouts.partials.sidebar-evento', ['evento' => $evento, 'ativo' => 'evento'])
@endsection

@section('content')

    <header class="page-header">
        <div>
            <h1 class="page-header__titulo">Editar Evento</h1>
            <div class="page-header__subtitulo">Atualize as informações de {{ $evento->nome_evento }}</div>
        </div>
    </header>

    <div class="form-wrapper">
        <form method="post" action="{{ route('eventos.update', $evento) }}" class="form-card">
            @csrf
            @method('PUT')

            <div class="form-grupo">
                <label for="nome_evento">Nome do evento</label>
                <input type="text" id="nome_evento" name="nome_evento" value="{{ old('nome_evento', $evento->nome_evento) }}">
            </div>

            <div class="form-linha">
                <div class="form-grupo">
                    <label for="tipo_evento">Tipo do evento</label>
                    <input type="text" id="tipo_evento" name="tipo_evento" value="{{ old('tipo_evento', $evento->tipo_evento) }}">
                </div>
                <div class="form-grupo">
                    <label for="data_evento">Data do evento</label>
                    <input type="date" id="data_evento" name="data_evento" value="{{ old('data_evento', $evento->data_evento) }}">
                </div>
            </div>

            <div class="form-grupo">
                <label for="endereco_evento">Endereço do evento</label>
                <input type="text" id="endereco_evento" name="endereco_evento" value="{{ old('endereco_evento', $evento->endereco_evento) }}">
            </div>

            <div class="form-grupo">
                <label for="orcamento_evento">Orçamento do evento (R$)</label>
                <input type="number" step="0.01" min="0" id="orcamento_evento" name="orcamento_evento" value="{{ old('orcamento_evento', $evento->orcamento_evento) }}">
            </div>

            <div class="form-acoes">
                <button type="submit" class="botao botao--primario">Salvar Alterações</button>
                <a href="{{ route('eventos.show', $evento) }}" class="botao botao--secundario">Cancelar</a>
            </div>
        </form>

        <form method="post" action="{{ route('eventos.destroy', $evento) }}" style="margin-top:16px" onsubmit="return confirm('Deseja realmente excluir este evento?');">
            @csrf
            @method('DELETE')
            <button type="submit" class="botao botao--perigo">Excluir evento</button>
        </form>
    </div>

@endsection
