""" apps/sejours/urls.py """

from django.urls import path, re_path

from . import views

app_name = 'sejours'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/$',
            views.calendar, name='calendar'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.details, name='details'),
    path('<int:pk>/update', views.update, name='update'),
    path('<int:pk>/delete', views.delete, name='delete'),
]
