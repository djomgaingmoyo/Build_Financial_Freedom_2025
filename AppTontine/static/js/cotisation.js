

// Fonction pour extraire les noms du couple
function extractNomsCouple(nomComplet) {
    const noms = nomComplet.replace('Couple ', '').split(' et ');
    return {
        beneficiaire1: noms[0]?.trim() || 'Membre 1',
        beneficiaire2: noms[1]?.trim() || 'Membre 2'
    };
}

// Fonction appelée quand la sélection change
function updateBeneficiaires(selectElement) {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    
    if (selectedOption.value) {
        const nomCouple = selectedOption.getAttribute('data-nom');
        const noms = extractNomsCouple(nomCouple);
        
        // Met à jour les labels
        document.getElementById('beneficiaire1').textContent = noms.beneficiaire1;
        document.getElementById('beneficiaire2').textContent = noms.beneficiaire2;
        
        // Active les champs de montant
        document.getElementById('montantMembre1').disabled = false;
        document.getElementById('montantMembre2').disabled = false;
    } else {
        // Réinitialise si aucun couple sélectionné
        document.getElementById('beneficiaire1').textContent = '[Sélectionnez un couple]';
        document.getElementById('beneficiaire2').textContent = '[Sélectionnez un couple]';
        document.getElementById('montantMembre1').disabled = true;
        document.getElementById('montantMembre2').disabled = true;
    }
}

// Initialisation quand la page est chargée
document.addEventListener('DOMContentLoaded', function() {
    // Désactive les champs de montant initialement
    document.getElementById('montantMembre1').disabled = true;
    document.getElementById('montantMembre2').disabled = true;
});

