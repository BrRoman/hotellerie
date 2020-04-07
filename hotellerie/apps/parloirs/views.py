""" apps/parloirs/views.py """

from django.shortcuts import render


def home(request):
    """ Home view of parloirs. """
    return render(request, 'parloirs/home.html', {})


def list(request):
    """ List of parloirs. """
    return render(request, 'parloirs/list.html', {})


def create(request):
    """ Create a Parloir. """
    return render(request, 'parloirs/form.html', {})


def details(request, *args, **kwargs):
    """ Details of a Parloir. """
    return render(request, 'parloirs/details.html', {'id_parloir': kwargs['pk']})


def update(request, *args, **kwargs):
    """ Update a Parloir. """
    return render(request, 'parloirs/form.html', {'id_parloir': kwargs['pk']})


def delete(request, *args, **kwargs):
    """ Delete a Parloir. """
    return render(request, 'parloirs/delete.html', {'id_parloir': kwargs['pk']})

