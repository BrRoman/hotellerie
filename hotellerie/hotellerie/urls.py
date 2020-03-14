""" hotellerie/urls.py """

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('hotellerie/', include('apps.sejours.urls')),
    path('admin/', admin.site.urls),
]
