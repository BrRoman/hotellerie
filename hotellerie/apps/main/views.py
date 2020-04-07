""" apps/main.views.py """

from django.shortcuts import render


def home(request):
    """ Home view of Hôtellerie. """
    return render(request, 'main/home.html', {})

