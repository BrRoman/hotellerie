""" hotellerie/urls.py """

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('hotellerie/', include('apps.sejours.urls')),
    path('hotellerie/accounts/', include('apps.accounts.urls')),
]
