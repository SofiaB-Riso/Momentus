(() => {
    try {document.documentElement.dataset.tema = localStorage.getItem('momentus:tema') || 'claro';}
    catch (_) {document.documentElement.dataset.tema = 'claro';}
})();
