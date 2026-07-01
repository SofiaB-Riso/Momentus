<?php $__env->startSection('titulo', 'Início'); ?>

<?php $__env->startSection('sidebar'); ?>
    <?php echo $__env->make('layouts.partials.sidebar-dashboard', ['ativo' => 'inicio'], array_diff_key(get_defined_vars(), ['__data' => 1, '__path' => 1]))->render(); ?>
<?php $__env->stopSection(); ?>

<?php $__env->startSection('content'); ?>

    <?php
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
    ?>

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
                    <a href="<?php echo e(route('eventos.create')); ?>">Planejar novo evento</a>
                </div>
            </details>
        </div>
    </header>

    <section class="grid-cards">
        <?php $__empty_1 = true; $__currentLoopData = $eventos; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $evento): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); $__empty_1 = false; ?>
            <article class="card card--evento">
                <div class="card-evento">
                    <div class="card-evento__topo">
                        <span class="card-evento__nome"><?php echo e($evento->nome_evento); ?></span>
                        <a href="<?php echo e(route('eventos.show', $evento)); ?>" class="card-evento__seta" title="Ver evento">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        </a>
                    </div>
                    <div class="card-evento__info">
                        <?php echo e($evento->endereco_evento); ?><br>
                        <?php echo e(\Carbon\Carbon::parse($evento->data_evento)->format('d/m')); ?> &bull; <?php echo e($evento->tipo_evento); ?>

                    </div>
                    <div class="card-evento__rodape">
                        Última alteração: <?php echo e(optional($evento->updated_at)->format('d/m/y \à\s H:i') ?? '—'); ?>

                    </div>
                </div>
            </article>
        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); if ($__empty_1): ?>
        <?php endif; ?>

        <a href="<?php echo e(route('eventos.create')); ?>" class="card card--tracejado">
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
                <span class="calendario__seletor"><?php echo e($meses[$hoje->month - 1]); ?> &nbsp; <?php echo e($hoje->year); ?></span>
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
                        <?php $__currentLoopData = array_chunk($celulas, 7); $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $semana): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                            <tr>
                                <?php $__currentLoopData = $semana; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $dia): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                                    <td>
                                        <?php if($dia): ?>
                                            <span class="calendario__dia
                                                <?php echo e($dia === $hoje->day ? 'is-selecionado' : ''); ?>

                                                <?php echo e(in_array($dia, $diasComEvento) && $dia !== $hoje->day ? 'is-evento' : ''); ?>">
                                                <?php echo e($dia); ?>

                                            </span>
                                        <?php endif; ?>
                                    </td>
                                <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                            </tr>
                        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                    </tbody>
                </table>

                <div class="calendario__eventos">
                    <?php $__empty_1 = true; $__currentLoopData = $proximosEventos; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $index => $item): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); $__empty_1 = false; ?>
                        <div class="calendario__evento-pill <?php echo e($index % 2 === 0 ? 'calendario__evento-pill--roxo' : 'calendario__evento-pill--rosa'); ?>">
                            <span class="calendario__evento-data"><?php echo e($item['data']->format('d')); ?> <?php echo e($meses[$item['data']->month - 1]); ?></span>
                            <span><?php echo e($item['evento']->tipo_evento); ?></span>
                        </div>
                    <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); if ($__empty_1): ?>
                        <div class="calendario__evento-vazio"></div>
                        <div class="calendario__evento-vazio"></div>
                    <?php endif; ?>
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
                            <?php for($i = 0; $i < 5; $i++): ?>
                                <svg class="<?php echo e($i < 2 ? '' : 'is-vazia'); ?>" width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3 6.5 7 .9-5.2 4.9 1.4 6.9L12 17.9 5.8 21.2l1.4-6.9L2 9.4l7-.9L12 2Z"/></svg>
                            <?php endfor; ?>
                        </div>
                    </div>
                </div>
                <div class="produto-card">
                    <div class="produto-card__thumb"></div>
                    <div>
                        <div class="produto-card__nome">Boquinha</div>
                        <div class="produto-card__categoria">Salgadinhos de festa</div>
                        <div class="produto-card__estrelas">
                            <?php for($i = 0; $i < 5; $i++): ?>
                                <svg class="<?php echo e($i < 3 ? '' : 'is-vazia'); ?>" width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3 6.5 7 .9-5.2 4.9 1.4 6.9L12 17.9 5.8 21.2l1.4-6.9L2 9.4l7-.9L12 2Z"/></svg>
                            <?php endfor; ?>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </section>

<?php $__env->stopSection(); ?>

<?php echo $__env->make('layouts.menu', array_diff_key(get_defined_vars(), ['__data' => 1, '__path' => 1]))->render(); ?><?php /**PATH C:\Users\Cicero\Downloads\Momentus1\resources\views/paginas/index.blade.php ENDPATH**/ ?>