""" apps/personnes/admin.py """

from django.contrib import admin
from .models import Adresse, Mail, Personne, Telephone

admin.site.register(Adresse)
admin.site.register(Mail)
admin.site.register(Personne)
admin.site.register(Telephone)
