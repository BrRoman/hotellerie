""" apps/parloirs/views.py """

import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required

from .forms import ParloirForm
from .models import Parloir


@login_required
def home(request):
    """ Home view of Parloirs = redirect to calendar with current date as parameter. """
    today = datetime.date.today()
    day = today.strftime('%d')
    month = today.strftime('%m')
    year = today.strftime('%Y')
    return redirect('parloirs:calendar', day=day, month=month, year=year)


@login_required
def calendar(request, *args, **kwargs):
    """ Display calendar of parloirs according to the required date. """
    parloirs = Parloir.objects.all()
    return render(request, 'parloirs/calendar.html', {'parloirs': parloirs})


@login_required
def create(request):
    """ Create a Parloir. """
    if request.method == 'POST':
        form = ParloirForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('parloirs:home'))

    else:
        form = ParloirForm()

    return render(request, 'parloirs/form.html', {'form': form})


@login_required
def details(request, *args, **kwargs):
    """ Details of a Parloir. """
    parloir = get_object_or_404(Parloir, id=kwargs['pk'])
    return render(request, 'parloirs/details.html', {'parloir': parloir})


@login_required
def update(request, *args, **kwargs):
    """ Update a Parloir. """
    parloir = get_object_or_404(Parloir, pk=kwargs['pk'])

    if request.method == 'POST':
        form = ParloirForm(request.POST, instance=parloir)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('parloirs:home'))

    else:
        form = ParloirForm(instance=parloir)

    return render(request, 'parloirs/form.html', {
        'form': form,
        'parloir': parloir,
    })


@login_required
def delete(request, *args, **kwargs):
    """ Delete a Parloir. """
    parloir = get_object_or_404(Parloir, pk=kwargs['pk'])

    if request.method == 'POST':
        form = ParloirForm(request.POST, instance=parloir)
        parloir.delete()
        return HttpResponseRedirect(reverse('parloirs:home'))

    else:
        form = ParloirForm(instance=parloir)

    return render(request, 'parloirs/delete.html', {
        'form': form,
        'parloir': parloir,
    })
