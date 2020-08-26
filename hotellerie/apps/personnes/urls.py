""" apps/personnes/urls.py """

from django.urls import path

from . import views

app_name = 'personnes'
urlpatterns = [
    path('list/<str:letter>/', views.list, name='list'),
    path('list/<str:letter>/<str:search>/', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.details, name='details'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('autocomplete/', views.PersonneAutocompleteView.as_view(),
         name='autocomplete'),
]
