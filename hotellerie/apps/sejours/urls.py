""" apps/sejours/urls.py """

from django.urls import path

from . import views

app_name = 'sejours'
urlpatterns = [
    path('', views.agenda, name='agenda'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.details, name='details'),
    path('<int:pk>/update', views.update, name='update'),
    path('<int:pk>/delete', views.delete, name='delete'),
]
