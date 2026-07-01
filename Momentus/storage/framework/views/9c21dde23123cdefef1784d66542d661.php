<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Momentus <?php if (! empty(trim($__env->yieldContent('titulo')))): ?>— <?php echo $__env->yieldContent('titulo'); ?><?php endif; ?></title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="<?php echo e(asset('css/layouts/menu.css')); ?>">
    <link rel="stylesheet" href="<?php echo e(asset('css/paginas/style.css')); ?>">
    <?php echo $__env->yieldPushContent('estilos'); ?>
</head>
<body>
    <div class="app">
        <?php echo $__env->yieldContent('sidebar'); ?>

        <main class="main">
            <?php if(session('successo')): ?>
                <div class="alerta alerta--sucesso"><?php echo e(session('successo')); ?></div>
            <?php endif; ?>
            <?php if(session('success')): ?>
                <div class="alerta alerta--sucesso"><?php echo e(session('success')); ?></div>
            <?php endif; ?>

            <?php echo $__env->yieldContent('content'); ?>
        </main>
    </div>
</body>
</html>
<?php /**PATH C:\Users\Cicero\Downloads\Momentus1\resources\views/layouts/menu.blade.php ENDPATH**/ ?>