""" apps/sejours/views.py """

import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import SejourForm
from .models import Chambre, Sejour


@login_required
def home(request):
    """ Home view of Sejours = redirect to calendar with current date as parameter. """
    today = datetime.date.today()
    day = today.strftime('%d')
    month = today.strftime('%m')
    year = today.strftime('%Y')
    return redirect('sejours:calendar', day=day, month=month, year=year)


@login_required
def calendar(request, *args, **kwargs):
    """ Display calendar of sejours according to the required date. """
    date_today = datetime.date.today()
    today = {'day': date_today.strftime(
        '%d'), 'month': date_today.strftime('%m'), 'year': date_today.strftime('%Y')}

    # Date that has been required in **kwargs:
    display_date = datetime.datetime(
        int(kwargs['year']), int(kwargs['month']), int(kwargs['day']))

    # Initial and last dates of the week containing the required date:
    initial_date = display_date - \
        datetime.timedelta(days=(display_date.weekday() + 1)
                           if display_date.weekday() != 6 else 0)
    initial_date_human = datetime.date(
        initial_date.year, initial_date.month, initial_date.day)

    # Construct the list of days with all their data:
    days = {}
    for i in range(7):
        coord_x = 0
        date = initial_date + datetime.timedelta(days=i)
        date_human = datetime.date(date.year, date.month, date.day)
        max_length = 7 - i

        days[date_human] = {}
        days[date_human]['current'] = (date_human == datetime.date.today())
        days[date_human]['sejours'] = {}

        sejours = Sejour.objects.filter(
            sejour_du__lte=date).filter(sejour_au__gte=date)
        for index, sejour in enumerate(sejours):
            arrow_left = sejour.sejour_du < initial_date_human
            arrow_right = sejour.sejour_au > (
                initial_date_human + datetime.timedelta(days=7))

            pretre = sejour.dit_messe

            chambres_nombre = sejour.chambre_set.count()
            chambres_queryset = Chambre.objects.filter(
                sejour=sejour).values('chambre')
            chambres_string = ''
            for chambre in chambres_queryset:
                chambres_string += (', ' if chambres_string !=
                                    '' else '') + chambre['chambre']

            if sejour.sejour_du == date_human:
                length = ((sejour.sejour_au - date_human).days + 1)
                coord_x = i + 1
            elif (sejour.sejour_du < date_human) and (sejour.sejour_au > (date_human + datetime.timedelta(days=7))) and (i == 0):
                length = 7
                coord_x = 1
            elif (sejour.sejour_au == date_human) and (sejour.sejour_du < initial_date_human):
                length = ((date_human - initial_date_human).days + 1)
                coord_x = 1
            else:
                length = 0

            if length > max_length:
                length = max_length

            days[date_human]['sejours'][sejour] = {
                'x': coord_x,
                'length': length,
                'arrow_left': arrow_left,
                'arrow_right': arrow_right,
                'pretre': pretre,
                'chambres_nombre': chambres_nombre,
                'chambres_string': chambres_string
            }

    return render(request, 'sejours/calendar.html', {
        'today': today,
        'days': days,
    })


@login_required
def create(request):
    """ Create a Sejour. """
    if request.method == 'POST':
        form = SejourForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sejours:home'))

    else:
        form = SejourForm()

    return render(request, 'sejours/form.html', {'form': form})


@login_required
def details(request, *args, **kwargs):
    """ Details of a Sejour. """
    sejour = get_object_or_404(Sejour, pk=kwargs['pk'])
    return render(request, 'sejours/details.html', {'sejour': sejour})


@login_required
def update(request, *args, **kwargs):
    """ Update a Sejour. """
    sejour = get_object_or_404(Sejour, pk=kwargs['pk'])

    if request.method == 'POST':
        form = SejourForm(request.POST, instance=sejour)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sejours:details', args=[sejour.id]))

    else:
        form = SejourForm(instance=sejour)

    return render(request, 'sejours/form.html', {
        'form': form,
        'sejour': sejour,
    })


@login_required
def delete(request, *args, **kwargs):
    """ Delete a Sejour. """
    sejour = get_object_or_404(Sejour, pk=kwargs['pk'])

    if request.method == 'POST':
        form = SejourForm(request.POST, instance=sejour)
        sejour.delete()
        return HttpResponseRedirect(reverse('sejours:home'))

    else:
        form = SejourForm(instance=sejour)

    return render(request, 'sejours/delete.html', {
        'form': form,
        'sejour': sejour,
    })
