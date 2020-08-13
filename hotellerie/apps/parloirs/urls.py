""" apps/parloirs/urls.py """

from django.urls import path, re_path

from . import views

app_name = 'parloirs'
urlpatterns = [
    path('', views.calendar, name='home'),
    re_path(r'^(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/$',
            views.calendar, name='calendar'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.details, name='details'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
