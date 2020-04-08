""" apps/parloirs/views.py """

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """ Home view of parloirs. """
    return render(request, 'parloirs/home.html', {})


@login_required
def list(request):
    """ List of parloirs. """
    return render(request, 'parloirs/list.html', {})


@login_required
def create(request):
    """ Create a Parloir. """
    return render(request, 'parloirs/form.html', {})


@login_required
def details(request, *args, **kwargs):
    """ Details of a Parloir. """
    return render(request, 'parloirs/details.html', {'id_parloir': kwargs['pk']})


@login_required
def update(request, *args, **kwargs):
    """ Update a Parloir. """
    return render(request, 'parloirs/form.html', {'id_parloir': kwargs['pk']})


@login_required
def delete(request, *args, **kwargs):
    """ Delete a Parloir. """
    return render(request, 'parloirs/delete.html', {'id_parloir': kwargs['pk']})
