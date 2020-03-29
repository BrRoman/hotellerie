""" apps/sejours/views.py """

from django.shortcuts import render


def home(request):
    """ Home view of Sejours. """
    return render(request, 'sejours/home.html', {})
