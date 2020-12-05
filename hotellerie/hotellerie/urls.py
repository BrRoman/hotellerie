""" hotellerie/urls.py """

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('hotellerie/', include('apps.main.urls')),
    path('hotellerie/accounts/', include('apps.accounts.urls')),
    path('hotellerie/personnes/', include('apps.personnes.urls')),
    path('hotellerie/sejours/', include('apps.sejours.urls')),
    path('hotellerie/parloirs/', include('apps.parloirs.urls')),
    path('hotellerie/listings/', include('apps.listings.urls')),
    path('hotellerie/admin/', admin.site.urls),
]
