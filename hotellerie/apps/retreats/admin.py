""" apps/retreats/admin.py """

from django.contrib import admin

from .models import Retreat

admin.site.register(Retreat)
