from django.shortcuts import render,redirect
from django.views.generic import ListView
from datetime import datetime

from .models import *

# Create your views here.
def home(request):
    return render(request, 'home.html')


def Cotiser(request):
    if request.method=='POST':

        # recuperation des couples et du payeur dans les tables (Couple,Membre) en fonction de la cle primaire 
        couple_beneficiaire=Couple.objects.get(pk=request.POST['C_beneficiaire'])
        payeur=Membre.objects.get(pk=request.POST['payeur'])
        mois_en_cours = datetime.now().month
        annee_en_cours = datetime.now().year
        tontine = Tontine.objects.get(annee=annee_en_cours)

        montant_total=request.POST['montantTotal']
        montant_membre1=request.POST['montantMembre1']
        montant_membre2=request.POST['montantMembre2']

        savedonnees = Cotisation(couple_beneficiaire=couple_beneficiaire,payeur=payeur,mois=mois_en_cours,tontine=tontine,montant_total=montant_total,montant_membre1=montant_membre1,montant_membre2=montant_membre2)
        savedonnees.save()
        return redirect('home')
    else:
        couple_beneficiaire=Couple.objects.all
        payeur=Membre.objects.all
    return render(request, 'Cotiser.html',{"couple_beneficiaire":couple_beneficiaire,"payeur":payeur})