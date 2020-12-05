""" apps/listings/urls.py """

from django.urls import path

from . import views

app_name = 'listings'
urlpatterns = [
    path('cuisine/', views.cuisine, name='cuisine'),
    path('hotellerie/', views.hotellerie, name='hotellerie'),
]
