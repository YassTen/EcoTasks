// script.js - JS minimal, juste ce qu'il faut
// Pas de framework, pas de jQuery, juste du vanilla

// Confirmation avant suppression d'une tache ou d'un compte
function confirmerSuppression() {
    return confirm('Supprimer cette tache ?');
}

// Mode sombre : on persiste le choix dans localStorage
// pour ne pas re-demander a chaque page
(function () {
    var theme = localStorage.getItem('theme');

    // Si pas de preference sauvegardee, on respecte la preference systeme
    if (!theme) {
        var prefereSombre = window.matchMedia('(prefers-color-scheme: dark)').matches;
        theme = prefereSombre ? 'sombre' : 'clair';
    }

    if (theme === 'sombre') {
        document.documentElement.setAttribute('data-theme', 'sombre');
    }
})();

document.addEventListener('DOMContentLoaded', function () {
    // Fermer les alertes flash apres 4 secondes
    var alertes = document.querySelectorAll('.alerte');
    if (alertes.length > 0) {
        setTimeout(function () {
            alertes.forEach(function (alerte) {
                alerte.style.opacity = '0';
                alerte.style.transition = 'opacity 0.3s';
                setTimeout(function () { alerte.remove(); }, 300);
            });
        }, 4000);
    }

    // Toggle mode sombre
    var btnTheme = document.getElementById('btn-theme');
    if (btnTheme) {
        btnTheme.addEventListener('click', function () {
            var html = document.documentElement;
            var estSombre = html.getAttribute('data-theme') === 'sombre';

            if (estSombre) {
                html.removeAttribute('data-theme');
                localStorage.setItem('theme', 'clair');
            } else {
                html.setAttribute('data-theme', 'sombre');
                localStorage.setItem('theme', 'sombre');
            }
        });
    }
});
