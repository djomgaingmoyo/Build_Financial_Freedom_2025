from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class Couple(models.Model):
    """
    Représente un couple de l'association (12 couples total)
    Contient exactement 2 membres (via la relation Membre.couple)
    """
    nom = models.CharField(
        max_length=100,
        unique=True,
        help_text="Format: 'Couple NOM1_MARI-NOM2_FEMME'"
    )
    date_creation = models.DateField(auto_now_add=True)
    adresse_couple = models.CharField(max_length=300)

    class Meta:
        ordering = ['nom']
        verbose_name = "Couple"
        verbose_name_plural = "Couples"

    def __str__(self):
        return self.nom

class Membre(models.Model):
    """
    Fiche individuelle d'un membre (24 membres = 12 × 2)
    Chaque membre appartient à un et un seul couple
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    date_adhesion = models.DateField(auto_now_add=True)
    couple = models.ForeignKey(
        Couple,
        on_delete=models.CASCADE,
        related_name='membres'
    )

    class Meta:
        ordering = ['user__last_name']
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        constraints = [
            models.UniqueConstraint(
                fields=['couple'],
                condition=models.Q(couple__isnull=False),
                name='max_2_membres_par_couple'
            )
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.couple.nom})"

class Tontine(models.Model):
    """
    Tontine annuelle avec 12 tours (1 par mois)
    """
    annee = models.PositiveIntegerField(
        unique=True,
        validators=[MinValueValidator(2024)]
    )
    nom = models.CharField(
        max_length=100,
        default="Tontine Annuelle"
    )
    description = models.TextField(blank=True)
    date_debut = models.DateField(editable=False)  # Auto: 1er janvier
    date_fin = models.DateField(editable=False)    # Auto: 31 décembre
    createur = models.ForeignKey(
        Membre,
        on_delete=models.PROTECT,
        related_name='tontines_crees'
    )

    def save(self, *args, **kwargs):
        self.date_debut = date(self.annee, 1, 1)
        self.date_fin = date(self.annee, 12, 31)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-annee']
        verbose_name = "Tontine"
        verbose_name_plural = "Tontines"

    def __str__(self):
        return f"{self.nom} {self.annee}"

class Participation(models.Model):
    """
    Attribution d'un mois à un couple bénéficiaire
    """
    couple = models.ForeignKey(
        Couple,
        on_delete=models.CASCADE,
        related_name='participations'
    )
    tontine = models.ForeignKey(
        Tontine,
        on_delete=models.CASCADE,
        related_name='participations'
    )
    ordre_reception = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Mois attribué (1=janvier, 12=décembre)"
    )

    class Meta:
        unique_together = [
            ('tontine', 'ordre_reception'),  # 1 couple par mois
            ('tontine', 'couple')           # 1 mois par couple
        ]
        ordering = ['tontine', 'ordre_reception']
        verbose_name = "Attribution"
        verbose_name_plural = "Attributions"

    def __str__(self):
        return f"{self.couple} - Mois {self.ordre_reception}"

class Cotisation(models.Model):
    """
    Paiement individuel d'un membre vers un couple bénéficiaire
    """
    tontine = models.ForeignKey(
        Tontine,
        on_delete=models.CASCADE,
        related_name='cotisations'
    )
    mois = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    payeur = models.ForeignKey(
        Membre,
        on_delete=models.CASCADE,
        related_name='cotisations_payees'
    )
    couple_beneficiaire = models.ForeignKey(
        Couple,
        on_delete=models.CASCADE,
        related_name='cotisations_recues'
    )
    montant_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    montant_membre1 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    montant_membre2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    date_paiement = models.DateField(auto_now_add=True)
    est_valide = models.BooleanField(default=False)

    def clean(self):
        """Valide la cohérence des montants"""
        from django.core.exceptions import ValidationError
        total_calculé = self.montant_membre1 + self.montant_membre2
        if total_calculé != self.montant_total:
            raise ValidationError(
                f"Erreur: {self.montant_membre1} + {self.montant_membre2} ≠ {self.montant_total}"
            )

    class Meta:
        unique_together = [
            ('tontine', 'mois', 'payeur', 'couple_beneficiaire')
        ]
        verbose_name = "Cotisation"
        verbose_name_plural = "Cotisations"

    def __str__(self):
        return f"{self.payeur} → {self.couple_beneficiaire} : {self.montant_total}€"

class ReceptionTontine(models.Model):
    """
    Bénéfice reçu par un couple avec répartition calculée
    """
    tontine = models.ForeignKey(
        Tontine,
        on_delete=models.CASCADE,
        related_name='receptions'
    )
    mois = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    couple_beneficiaire = models.ForeignKey(
        Couple,
        on_delete=models.CASCADE,
        related_name='receptions'
    )
    montant_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False
    )
    montant_membre1 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )
    montant_membre2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )
    date_reception = models.DateField()
    est_confirme = models.BooleanField(default=False)

    def calculer_montants(self):
        """Agrège toutes les cotisations valides"""
        cotisations = Cotisation.objects.filter(
            tontine=self.tontine,
            mois=self.mois,
            couple_beneficiaire=self.couple_beneficiaire,
            est_valide=True
        )
        self.montant_membre1 = sum(c.montant_membre1 for c in cotisations)
        self.montant_membre2 = sum(c.montant_membre2 for c in cotisations)
        self.montant_total = self.montant_membre1 + self.montant_membre2

    def save(self, *args, **kwargs):
        self.calculer_montants()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = [('tontine', 'mois')]
        verbose_name = "Réception"
        verbose_name_plural = "Réceptions"

    def __str__(self):
        return f"{self.couple_beneficiaire} - Mois {self.mois} : {self.montant_total}€"
