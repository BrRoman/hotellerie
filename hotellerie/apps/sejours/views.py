""" apps/sejours/views.py """

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """ Home view of Sejours. """
    return render(request, 'sejours/home.html', {})


@login_required
def agenda(request):
    """ Main page of Sejours. """
    return render(request, 'sejours/agenda.html', {})


@login_required
def create(request):
    """ Create a Sejour. """
    return render(request, 'sejours/form.html', {})


@login_required
def details(request, *args, **kwargs):
    """ Details of a Sejour. """
    return render(request, 'sejours/details.html', {'id_sejour': kwargs['pk']})


@login_required
def update(request, *args, **kwargs):
    """ Update a Sejour. """
    return render(request, 'sejours/form.html', {'id_sejour': kwargs['pk']})


@login_required
def delete(request, *args, **kwargs):
    """ Delete a Sejour. """
    return render(request, 'sejours/delete.html', {'id_sejour': kwargs['pk']})

