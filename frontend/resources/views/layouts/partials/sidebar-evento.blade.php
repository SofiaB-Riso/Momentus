{{-- Sidebar usada dentro do contexto de um evento (visualizar / editar) --}}
<aside class="sidebar">

    <div class="sidebar__logo">
        <svg class="sidebar__logo-icone" width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M6 3H18M6 21H18M7 3C7 8 11 9.5 12 10.5C13 9.5 17 8 17 3M7 21C7 16 11 14.5 12 13.5C13 14.5 17 16 17 21" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="sidebar__logo-texto">Momentus</span>
    </div>

    <nav class="sidebar__nav">
        <a href="{{ route('eventos.show', $evento) }}" class="sidebar__link sidebar__link--evento {{ ($ativo ?? '') === 'evento' ? 'is-active' : '' }}">
            {{ $evento->nome_evento }}
        </a>

        <div class="sidebar__separador"></div>

        <a href="{{ route('eventos.show', $evento) }}#planejamento" class="sidebar__link">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M3 10h18M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
            <span>Planejamento</span>
        </a>
        <a href="{{ route('eventos.show', $evento) }}#orcamento" class="sidebar__link">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v10M9.5 9.5c0-1.1 1.1-2 2.5-2s2.5.7 2.5 1.8c0 2.4-5 1.2-5 3.6 0 1.1 1.1 1.8 2.5 1.8s2.5-.9 2.5-2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            <span>Orçamento</span>
        </a>
        <a href="#" class="sidebar__link">
            <span style="width:17px;display:inline-block"></span>
            <span>Fornecedores</span>
        </a>
        <a href="#" class="sidebar__link">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><circle cx="9" cy="8" r="3.2" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 20c.6-3.4 3-5.4 5.5-5.4s4.9 2 5.5 5.4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="17" cy="9" r="2.6" stroke="currentColor" stroke-width="1.6"/><path d="M15.3 14.8c2.1.3 3.9 2 4.4 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
            <span>Convidados</span>
        </a>
        <a href="#" class="sidebar__link">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><path d="M20 6.5 9 17.5l-5-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span>Tarefas</span>
        </a>
    </nav>

    <div class="sidebar__spacer"></div>

    <a href="{{ route('eventos.index') }}" class="sidebar__voltar" title="Voltar para o início">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M14 5l-7 7 7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
</aside>
