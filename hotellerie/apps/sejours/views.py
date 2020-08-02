""" apps/sejours/views.py """

import datetime

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Sejour


@login_required
def home(request):
    """ Home view of Sejours = redirect to calendar with current date as paramter. """
    today = datetime.date.today()
    day = today.strftime('%d')
    month = today.strftime('%m')
    year = today.strftime('%Y')
    return redirect('sejours:calendar', day=day, month=month, year=year)


@login_required
def calendar(request, *args, **kwargs):
    """ Display calendar according to the required date. """
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

    # Construct the list of days with all their data:
    days = {}
    for i in range(7):
        date = initial_date + datetime.timedelta(days=i)
        date_human = datetime.date(date.year, date.month, date.day)

        days[date_human] = {}
        days[date_human]['current'] = (date_human == datetime.date.today())
        days[date_human]['sejours'] = {}

        sejours = Sejour.objects.filter(
            sejour_du__lte=date).filter(sejour_au__gte=date)
        for index, sejour in enumerate(sejours):
            is_beginning = (sejour.sejour_du == date_human)
            length = ((sejour.sejour_au - date_human).days +
                      1) if is_beginning else 0
            days[date_human]['sejours'][sejour] = {
                'x': index + 1,
                'length': length
            }

    return render(request, 'sejours/calendar.html', {
        'today': today,
        'days': days,
    })


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
