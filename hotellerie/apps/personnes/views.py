""" apps/personnes/views.py """

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """ Home view of Personnes. """
    return render(request, 'personnes/home.html', {})


@login_required
def list(request):
    """ List of Personnes. """
    return render(request, 'personnes/list.html', {})


@login_required
def create(request):
    """ Create a Personne. """
    return render(request, 'personnes/form.html', {})


@login_required
def details(request, *args, **kwargs):
    """ Details of a Personne. """
    return render(request, 'personnes/details.html', {'id_personne': kwargs['pk']})


@login_required
def update(request, *args, **kwargs):
    """ Update a Personne. """
    return render(request, 'personnes/form.html', {'id_personne': kwargs['pk']})


@login_required
def delete(request, *args, **kwargs):
    """ Delete a Personne. """
    return render(request, 'personnes/delete.html', {'id_personne': kwargs['pk']})
