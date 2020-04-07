""" apps/sejours/views.py """

from django.shortcuts import render


def home(request):
    """ Home view of Sejours. """
    return render(request, 'sejours/home.html', {})


def agenda(request):
    """ Main page of Sejours. """
    return render(request, 'sejours/agenda.html', {})


def create(request):
    """ Create a Sejour. """
    return render(request, 'sejours/form.html', {})


def details(request, *args, **kwargs):
    """ Details of a Sejour. """
    return render(request, 'sejours/details.html', {'id_sejour': kwargs['pk']})


def update(request, *args, **kwargs):
    """ Update a Sejour. """
    return render(request, 'sejours/form.html', {'id_sejour': kwargs['pk']})


def delete(request, *args, **kwargs):
    """ Delete a Sejour. """
    return render(request, 'sejours/delete.html', {'id_sejour': kwargs['pk']})

