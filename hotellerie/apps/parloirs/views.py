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
    # Date that has been required in **kwargs:
    display_date = datetime.datetime(
        int(kwargs['year']), int(kwargs['month']), int(kwargs['day']))

    # Initial date of the week containing the required date:
    initial_date = display_date - \
        datetime.timedelta(days=(display_date.weekday() + 1)
                           if display_date.weekday() != 6 else 0)

    # Construct the list of days with all their data:
    days = {}
    for i in range(7):
        date = initial_date + datetime.timedelta(days=i)
        date_human = datetime.date(date.year, date.month, date.day)

        days[date_human] = {}
        days[date_human]['current'] = (date_human == datetime.date.today())
        days[date_human]['parloirs'] = Parloir.objects.filter(
            date=date).order_by('-date')

    return render(request, 'parloirs/calendar.html', {'days': days})


@login_required
def create(request):
    """ Create a Parloir. """
    if request.method == 'POST':
        form = ParloirForm(request.POST)
        if form.is_valid():
            form.save()
            date = form.cleaned_data['date']
            return HttpResponseRedirect(reverse('parloirs:calendar', kwargs={
                'day': '{:%d}'.format(date),
                'month': '{:%m}'.format(date),
                'year': '{:%Y}'.format(date),
            }))

    else:
        form = ParloirForm()

    return render(request, 'parloirs/form.html', {'form': form})


@login_required
def details(request, *args, **kwargs):
    """ Details of a Parloir. """
    parloir = get_object_or_404(Parloir, id=kwargs['pk'])

    return render(request, 'parloirs/details.html', {
        'parloir': parloir,
        'calendar_day': parloir.date.strftime('%d'),
        'calendar_month': parloir.date.strftime('%m'),
        'calendar_year': parloir.date.strftime('%Y')
    })


@login_required
def update(request, *args, **kwargs):
    """ Update a Parloir. """
    parloir = get_object_or_404(Parloir, pk=kwargs['pk'])

    if request.method == 'POST':
        form = ParloirForm(request.POST, instance=parloir)
        if form.is_valid():
            form.save()
            date = form.cleaned_data['date']
            return HttpResponseRedirect(reverse('parloirs:details', kwargs={'pk': parloir.id}))
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
