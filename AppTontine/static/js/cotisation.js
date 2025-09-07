


// Fonction pour extraire les noms du couple
function extractNomsCouple(nomComplet) {
    // Vérification et extraction plus robuste
    if (!nomComplet) return { beneficiaire1: 'Membre 1', beneficiaire2: 'Membre 2' };
    
    const noms = nomComplet.replace('Couple ', '').split(' et ');
    return {
        beneficiaire1: noms[0]?.trim() || 'Membre 1',
        beneficiaire2: noms[1]?.trim() || 'Membre 2'
    };
}

// Fonction appelée quand la sélection change
function updateBeneficiaires(selectElement) {
    console.log('Fonction appelée'); // Debug
    
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    console.log('Option sélectionnée:', selectedOption.value); // Debug
    
    if (selectedOption.value && selectedOption.value !== "") {
        const nomCouple = selectedOption.getAttribute('data-nom');
        console.log('Nom du couple:', nomCouple); // Debug
        
        const noms = extractNomsCouple(nomCouple);
        console.log('Noms extraits:', noms); // Debug
        
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
    console.log('Page chargée'); // Debug
    
    // Désactive les champs de montant initialement
    document.getElementById('montantMembre1').disabled = true;
    document.getElementById('montantMembre2').disabled = true;
    
    // Ajoute un écouteur d'événement pour tester
    document.getElementById('C_beneficiaire').addEventListener('change', function() {
        console.log('Change event triggered'); // Debug
        updateBeneficiaires(this);
    });
});

