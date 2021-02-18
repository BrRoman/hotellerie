""" apps/sejours/views.py """

import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from modules.mails import mail_pere_suiveur, mail_sacristie

from apps.retreats.models import Retreat

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

        days[date_human] = {}
        days[date_human]['current'] = (date_human == datetime.date.today())
        days[date_human]['retreats'] = {}
        days[date_human]['sejours'] = {}

        # Retreats:
        retreats = Retreat.objects.filter(
            date_from__lte=date)
        for index, retreat in enumerate(retreats):
            if retreat.date_to() >= initial_date_human:
                days[date_human]['retreats'][retreat] = {
                    'x': 2,
                    'length': 5,
                }

        # Séjours:
        sejours = Sejour.objects.filter(
            sejour_du__lte=date).filter(sejour_au__gte=date)
        for index, sejour in enumerate(sejours):
            # Arrows:
            arrow_left = sejour.sejour_du < initial_date_human
            arrow_right = sejour.sejour_au > (
                initial_date_human + datetime.timedelta(days=6))

            # Priest:
            pretre = sejour.dit_messe

            # Rooms:
            chambres_nombre = sejour.chambre_set.count()
            chambres_string = sejour.chambres_string()

            # Length and coord_x:
            length_to_subtract_du = length_to_subtract_au = 0
            # Length to subtract at the beginning of the bar depending on repas_du:
            if not sejour.sejour_du < initial_date_human:
                if sejour.repas_du == 'Petit-déjeuner':
                    length_to_subtract_du = 0
                elif sejour.repas_du == 'Déjeuner':
                    length_to_subtract_du = 1
                elif sejour.repas_du == 'Dîner':
                    length_to_subtract_du = 2
            # Length to subtract at the end of the bar depending on repas_au:
            if not sejour.sejour_au > (initial_date_human + datetime.timedelta(days=6)):
                if sejour.repas_au == 'Petit-déjeuner':
                    length_to_subtract_au = 2
                elif sejour.repas_au == 'Déjeuner':
                    length_to_subtract_au = 1
                elif sejour.repas_au == 'Dîner':
                    length_to_subtract_au = 0

            # Max length allowed to the bar:
            max_length = 21 if (sejour.sejour_du < date_human) \
                else (7 - i) * 3

            if sejour.sejour_du == date_human:
                length = (((sejour.sejour_au - date_human).days + 1) * 3)
                coord_x = (i * 3) + 1 + length_to_subtract_du
            elif (sejour.sejour_du < date_human) \
                    and (sejour.sejour_au > (date_human + datetime.timedelta(days=7))) \
                    and (i == 0):
                length = 21
                coord_x = 1
            elif (sejour.sejour_au == date_human) and (sejour.sejour_du < initial_date_human):
                length = (((date_human - initial_date_human).days + 1) * 3)
                coord_x = 1
            else:
                length = 0

            if length >= max_length:
                length = max_length
            else:
                length = length - length_to_subtract_du - length_to_subtract_au

            # Warnings about mails:
            warning_pere_suiveur = warning_sacristie = False
            if (sejour.personne.pere_suiveur is not None) and (not sejour.mail_pere_suiveur):
                warning_pere_suiveur = True
            if pretre and not sejour.mail_sacristie:
                warning_sacristie = True

            days[date_human]['sejours'][sejour] = {
                'x': coord_x,
                'length': length,
                'arrow_left': arrow_left,
                'arrow_right': arrow_right,
                'pretre': pretre,
                'chambres_nombre': chambres_nombre,
                'chambres_string': chambres_string,
                'warning_pere_suiveur': warning_pere_suiveur,
                'warning_sacristie': warning_sacristie,
            }

    return render(request, 'sejours/calendar.html', {
        'today': today,
        'days': days,
        'lines': range(21),
        'bold_lines': [2, 5, 8, 11, 14, 17, 20],
    })


@login_required
def create(request):
    """ Create a Sejour. """
    if request.method == 'POST':
        form = SejourForm(request.POST)

        if form.is_valid():
            sejour = form.save()

            # Create rooms:
            for chambre in form.cleaned_data['chambre']:
                Chambre.objects.create(sejour=sejour, chambre=chambre)

            # Send mails:
            if sejour.dit_messe and sejour.mail_sacristie:
                mail_sacristie(sejour)
            if sejour.personne and sejour.mail_pere_suiveur:
                mail_pere_suiveur(sejour)

            date = form.cleaned_data['sejour_du']
            return HttpResponseRedirect(reverse('sejours:calendar', kwargs={
                'day': '{:%d}'.format(date),
                'month': '{:%m}'.format(date),
                'year': '{:%Y}'.format(date),
            }))

    else:
        form = SejourForm()

    return render(request, 'sejours/form.html', {'form': form})


@login_required
def details(request, *args, **kwargs):
    """ Details of a Sejour. """
    sejour = get_object_or_404(Sejour, pk=kwargs['pk'])
    return render(request, 'sejours/details.html', {
        'sejour': sejour,
        'calendar_day': sejour.sejour_du.strftime('%d'),
        'calendar_month': sejour.sejour_du.strftime('%m'),
        'calendar_year': sejour.sejour_du.strftime('%Y'),
        'chambres': ', '.join(list(Chambre.objects.filter(
            sejour=sejour.id).values_list('chambre', flat=True))),
    })


@login_required
def update(request, **kwargs):
    """ Update a Sejour. """
    sejour = get_object_or_404(Sejour, pk=kwargs['pk'])

    if request.method == 'POST':
        form = SejourForm(request.POST, instance=sejour)

        if form.is_valid():
            form.save()

            # Remove old rooms and insert new ones:
            Chambre.objects.filter(sejour=sejour).delete()
            for chambre in form.cleaned_data['chambre']:
                Chambre.objects.create(sejour=sejour, chambre=chambre)

            # Send mails:
            if sejour.dit_messe and sejour.mail_sacristie:
                mail_sacristie(sejour)
            if sejour.personne and sejour.mail_pere_suiveur:
                mail_pere_suiveur(sejour)

            return HttpResponseRedirect(reverse('sejours:details', kwargs={'pk': sejour.id}))

    else:
        chambres = list(Chambre.objects.filter(
            sejour=sejour.id).values_list('chambre', flat=True))
        form = SejourForm(
            instance=sejour,
            initial={
                'chambre': chambres,
            }
        )

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


def get_rooms_status(request):
    """ Returns the rooms' status between sejour_du and sejour_au. """
    # Get data from JS:
    id_sejour = int(request.GET['id_sejour'])
    start_raw = request.GET['start']
    start_split = start_raw.split('/')
    start = datetime.date(
        int(start_split[2]), int(start_split[1]), int(start_split[0])
    )
    end_raw = request.GET['end']
    end_split = end_raw.split('/')
    end = datetime.date(
        int(end_split[2]), int(end_split[1]), int(end_split[0])
    )

    # Create the rooms' dict:
    rooms = {}
    for i in range(27):
        rooms[str(i)] = {
            'occupied': '',
            'title': '',
        }
    rooms['Chambre de l\'évêque'] = {
        'occupied': '',
        'title': '',
    }

    # Get sejours having a day between start and end:
    sejours_du_inside = Sejour.objects.filter(
        sejour_du__gte=start
    ).filter(
        sejour_du__lte=end
    )
    sejours_au_inside = Sejour.objects.filter(
        sejour_au__gte=start
    ).filter(
        sejour_au__lte=end
    )
    sejours_before_and_after = Sejour.objects.filter(
        sejour_du__lte=start
    ).filter(
        sejour_au__gte=end
    )
    sejours = sejours_du_inside.union(
        sejours_au_inside,
        sejours_before_and_after
    )

    for i, sejour in enumerate(sejours):
        chambres = Chambre.objects.filter(sejour=sejour)
        if sejour.pk != id_sejour:
            for j, chambre in enumerate(chambres):
                rooms[chambre.chambre]['occupied'] = True
                rooms[chambre.chambre]['title'] += '{}\n'.format(sejour)

    return JsonResponse(rooms)
