""" apps/sejours/admin.py """

from django.contrib import admin
from .models import Chambre, Sejour

admin.site.register(Chambre)
admin.site.register(Sejour)
