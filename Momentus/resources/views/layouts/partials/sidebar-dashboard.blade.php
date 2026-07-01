{{-- Sidebar geral do sistema, usada nas telas de listagem e criação --}}
<aside class="sidebar">

    <div class="sidebar__logo">
        <svg class="sidebar__logo-icone" width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M6 3H18M6 21H18M7 3C7 8 11 9.5 12 10.5C13 9.5 17 8 17 3M7 21C7 16 11 14.5 12 13.5C13 14.5 17 16 17 21" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="sidebar__logo-texto">Momentus</span>
    </div>

    @if (session('notificacao'))
        <div class="sidebar__aviso">
            <strong>Notificação:</strong> {{ session('notificacao') }}
        </div>
    @endif

    <nav class="sidebar__nav">
        <a href="{{ route('eventos.index') }}" class="sidebar__link {{ ($ativo ?? '') === 'inicio' ? 'is-active' : '' }}">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><path d="M4 11.5L12 4l8 7.5M6 10v9a1 1 0 0 0 1 1h3v-5a2 2 0 0 1 2-2h0a2 2 0 0 1 2 2v5h3a1 1 0 0 0 1-1v-9" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span>Início</span>
        </a>
        <a href="{{ route('eventos.create') }}" class="sidebar__link {{ ($ativo ?? '') === 'planejar' ? 'is-active' : '' }}">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M12 8v8M8 12h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
            <span>Planejar evento</span>
        </a>
        <a href="#" class="sidebar__link">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><path d="M4 7l8-4 8 4-8 4-8-4Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M4 7v10l8 4 8-4V7" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
            <span>Catálogo</span>
        </a>
        <a href="#" class="sidebar__link">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.6"/><path d="M19 12a7 7 0 0 0-.1-1.2l2-1.5-2-3.4-2.3.9a7 7 0 0 0-2.1-1.2L14 3h-4l-.4 2.6a7 7 0 0 0-2.1 1.2l-2.3-.9-2 3.4 2 1.5A7 7 0 0 0 5 12c0 .4 0 .8.1 1.2l-2 1.5 2 3.4 2.3-.9c.6.5 1.3.9 2.1 1.2L10 21h4l.4-2.6a7 7 0 0 0 2.1-1.2l2.3.9 2-3.4-2-1.5c.1-.4.2-.8.2-1.2Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>
            <span>Configurações</span>
        </a>
    </nav>

    <div class="sidebar__spacer"></div>
</aside>
