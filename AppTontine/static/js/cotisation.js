


// Fonction pour extraire les noms du couple
function extractNomsCouple(nomComplet) {
    console.log('Nom complet reçu:', nomComplet);
    if (!nomComplet) return { beneficiaire1: 'Membre 1', beneficiaire2: 'Membre 2' };
    
    // Méthode plus robuste pour extraire les noms
    const noms = nomComplet.replace(/^Couple\s+/i, '').split(/\s+et\s+/);
    console.log('Noms après split:', noms);
    
    return {
        beneficiaire1: noms[0]?.trim() || 'Membre 1',
        beneficiaire2: noms[1]?.trim() || 'Membre 2'
    };
}

// Fonction appelée quand la sélection change
function updateBeneficiaires(selectElement) {
    console.log('=== updateBeneficiaires appelée ===');
    console.log('Element sélectionné:', selectElement);
    console.log('Valeur sélectionnée:', selectElement.value);
    
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    console.log('Option complète:', selectedOption);
    
    if (selectedOption.value && selectedOption.value !== "") {
        const nomCouple = selectedOption.getAttribute('data-nom');
        console.log('Data-nom trouvé:', nomCouple);
        
        if (nomCouple) {
            const noms = extractNomsCouple(nomCouple);
            console.log('Noms extraits:', noms);
            
            // Met à jour les labels
            const benef1 = document.getElementById('beneficiaire1');
            const benef2 = document.getElementById('beneficiaire2');
            
            if (benef1 && benef2) {
                benef1.textContent = noms.beneficiaire1;
                benef2.textContent = noms.beneficiaire2;
                
                // Active les champs de montant
                document.getElementById('montantMembre1').disabled = false;
                document.getElementById('montantMembre2').disabled = false;
            } else {
                console.error('Elements beneficiaire1 ou beneficiaire2 non trouvés');
            }
        } else {
            console.error('Attribut data-nom non trouvé sur l\'option');
        }
    } else {
        console.log('Aucune valeur sélectionnée');
        // Réinitialise si aucun couple sélectionné
        document.getElementById('beneficiaire1').textContent = '[Sélectionnez un couple]';
        document.getElementById('beneficiaire2').textContent = '[Sélectionnez un couple]';
        document.getElementById('montantMembre1').disabled = true;
        document.getElementById('montantMembre2').disabled = true;
    }
}

// Initialisation quand la page est chargée
function initCotisation() {
    console.log('=== Initialisation de la page cotisation ===');
    
    // Vérifie que les éléments existent
    const selectElement = document.getElementById('C_beneficiaire');
    const montant1 = document.getElementById('montantMembre1');
    const montant2 = document.getElementById('montantMembre2');
    
    if (selectElement && montant1 && montant2) {
        console.log('Tous les éléments trouvés');
        
        // Désactive les champs de montant initialement
        montant1.disabled = true;
        montant2.disabled = true;
        
        // Ajoute l'écouteur d'événement
        selectElement.addEventListener('change', function() {
            console.log('Événement change détecté');
            updateBeneficiaires(this);
        });
        
        // Teste avec la première option si elle est sélectionnée
        if (selectElement.value && selectElement.selectedIndex > 0) {
            updateBeneficiaires(selectElement);
        }
    } else {
        console.error('Éléments manquants:', {
            select: !!selectElement,
            montant1: !!montant1,
            montant2: !!montant2
        });
    }
}

// Lance l'initialisation quand la page est prête
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCotisation);
} else {
    initCotisation();
}