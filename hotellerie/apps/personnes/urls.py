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
    path('get_pere_suiveur/', views.get_pere_suiveur, name='get_pere_suiveur'),
    path(
        'autocomplete_hotes/',
        views.PersonneAutocompleteHotesView.as_view(),
        name='autocomplete_hotes'
    ),
    path(
        'autocomplete_monks/',
        views.PersonneAutocompleteMonksView.as_view(),
        name='autocomplete_monks'
    ),
]
