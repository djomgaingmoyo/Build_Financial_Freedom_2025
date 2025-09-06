
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

# (Url, fonction, nom de la page html)
urlpatterns = [
    path('',home,name='home'),
    path('Cotiser/',Cotiser,name='Cotiser'),
    
    
]
