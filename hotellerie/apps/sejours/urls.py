""" apps/sejours/urls.py """

from django.urls import path

from . import views

app_name = 'sejours'
urlpatterns = [
    path('', views.SejoursHomeView.as_view(), name='home'),
]
