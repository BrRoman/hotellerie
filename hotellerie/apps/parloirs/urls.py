""" apps/parloirs/urls.py """

from django.urls import path

from . import views

app_name = 'parloirs'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.details, name='details'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
