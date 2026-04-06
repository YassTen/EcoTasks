// script.js - JS minimal, juste ce qu'il faut
// Pas de framework, pas de jQuery, juste du vanilla

// Confirmation avant suppression d'une tâche ou d'un compte
function confirmerSuppression() {
    return confirm('Supprimer cette tâche ?');
}

// Fermer les alertes flash après 4 secondes
// On attend que la page soit chargée pour pas bloquer le rendu
document.addEventListener('DOMContentLoaded', function () {
    var alertes = document.querySelectorAll('.alerte');
    if (alertes.length > 0) {
        setTimeout(function () {
            alertes.forEach(function (alerte) {
                alerte.style.opacity = '0';
                alerte.style.transition = 'opacity 0.3s';
                // on retire du DOM après la transition
                setTimeout(function () { alerte.remove(); }, 300);
            });
        }, 4000);
    }
});
