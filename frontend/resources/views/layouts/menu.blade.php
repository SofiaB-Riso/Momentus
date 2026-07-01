<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Momentus @hasSection('titulo')— @yield('titulo')@endif</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="{{ asset('css/layouts/menu.css') }}">
    <link rel="stylesheet" href="{{ asset('css/paginas/style.css') }}">
    @stack('estilos')
</head>
<body>
    <div class="app">
        @yield('sidebar')

        <main class="main">
            @if (session('successo'))
                <div class="alerta alerta--sucesso">{{ session('successo') }}</div>
            @endif
            @if (session('success'))
                <div class="alerta alerta--sucesso">{{ session('success') }}</div>
            @endif

            @yield('content')
        </main>
    </div>
</body>
</html>
