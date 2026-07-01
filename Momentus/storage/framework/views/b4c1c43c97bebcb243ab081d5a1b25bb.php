<?php $__env->startSection('titulo', 'Criar evento'); ?>

<?php $__env->startSection('sidebar'); ?>
    <?php echo $__env->make('layouts.partials.sidebar-dashboard', ['ativo' => 'planejar'], array_diff_key(get_defined_vars(), ['__data' => 1, '__path' => 1]))->render(); ?>
<?php $__env->stopSection(); ?>

<?php $__env->startSection('content'); ?>

    <header class="page-header">
        <div>
            <h1 class="page-header__titulo">Criação de Evento</h1>
            <div class="page-header__subtitulo">Preencha os dados abaixo para planejar um novo momento</div>
        </div>
    </header>

    <div class="form-wrapper">
        <form method="post" action="<?php echo e(route('eventos.store')); ?>" class="form-card">
            <?php echo csrf_field(); ?>

            <div class="form-grupo">
                <label for="nome_evento">Nome do evento</label>
                <input type="text" id="nome_evento" name="nome_evento" placeholder="Ex: Aniversário da Sofia" value="<?php echo e(old('nome_evento')); ?>">
            </div>

            <div class="form-linha">
                <div class="form-grupo">
                    <label for="tipo_evento">Tipo do evento</label>
                    <input type="text" id="tipo_evento" name="tipo_evento" placeholder="Ex: Aniversário, Casamento..." value="<?php echo e(old('tipo_evento')); ?>">
                </div>
                <div class="form-grupo">
                    <label for="data_evento">Data do evento</label>
                    <input type="date" id="data_evento" name="data_evento" value="<?php echo e(old('data_evento')); ?>">
                </div>
            </div>

            <div class="form-grupo">
                <label for="endereco_evento">Endereço do evento</label>
                <input type="text" id="endereco_evento" name="endereco_evento" placeholder="Rua, número, bairro, cidade" value="<?php echo e(old('endereco_evento')); ?>">
            </div>

            <div class="form-grupo">
                <label for="orcamento_evento">Orçamento do evento (R$)</label>
                <input type="number" step="0.01" min="0" id="orcamento_evento" name="orcamento_evento" placeholder="0,00" value="<?php echo e(old('orcamento_evento')); ?>">
            </div>

            <div class="form-acoes">
                <button type="submit" class="botao botao--primario">Criar Evento</button>
                <a href="<?php echo e(route('eventos.index')); ?>" class="botao botao--secundario">Cancelar</a>
            </div>
        </form>
    </div>

<?php $__env->stopSection(); ?>

<?php echo $__env->make('layouts.menu', array_diff_key(get_defined_vars(), ['__data' => 1, '__path' => 1]))->render(); ?><?php /**PATH C:\Users\Cicero\Downloads\Momentus1\resources\views/paginas/criar-evento.blade.php ENDPATH**/ ?>