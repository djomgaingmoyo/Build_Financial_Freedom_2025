
from django.urls import path
from .views import *

# (Url, fonction, nom de la page html)
urlpatterns = [
    path('',home,name='home'),
    path('Cotiser/',Cotiser,name='Cotiser'),
    
    
]
