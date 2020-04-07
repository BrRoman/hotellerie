""" apps/personnes/views.py """

from django.shortcuts import render


def home(request):
    """ Home view of Personnes. """
    return render(request, 'personnes/home.html', {})


def list(request):
    """ List of Personnes. """
    return render(request, 'personnes/list.html', {})


def create(request):
    """ Create a Personne. """
    return render(request, 'personnes/form.html', {})


def details(request, *args, **kwargs):
    """ Details of a Personne. """
    return render(request, 'personnes/details.html', {'id_personne': kwargs['pk']})


def update(request, *args, **kwargs):
    """ Update a Personne. """
    return render(request, 'personnes/form.html', {'id_personne': kwargs['pk']})


def delete(request, *args, **kwargs):
    """ Delete a Personne. """
    return render(request, 'personnes/delete.html', {'id_personne': kwargs['pk']})

