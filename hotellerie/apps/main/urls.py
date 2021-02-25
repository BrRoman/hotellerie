""" apps/main/urls.py """

from django.urls import path, re_path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendar, name='calendar'),
    re_path(r'^calendar/(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/$',
            views.calendar, name='calendar'),
]
