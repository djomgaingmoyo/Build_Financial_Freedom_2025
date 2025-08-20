from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Couple)
admin.site.register(Membre)
admin.site.register(Tontine)
admin.site.register(Participation)
admin.site.register(Cotisation)
admin.site.register(ReceptionTontine)
