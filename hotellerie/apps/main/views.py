""" apps/main.views.py """

import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.parloirs.models import Parloir
from apps.retreats.models import Retreat
from apps.sejours.models import Sejour


@login_required
def calendar(request, *args, **kwargs):
    """ Display calendar according to the required date. """
    date_today = datetime.date.today()
    today = {
        'day': date_today.strftime('%d'),
        'month': date_today.strftime('%m'),
        'year': date_today.strftime('%Y')
    }

    if kwargs:
        # Date that has been required in **kwargs:
        display_date = datetime.datetime(
            int(kwargs['year']), int(kwargs['month']), int(kwargs['day']))
    else:
        # Redirect to today:
        return redirect(reverse(
            'main:calendar',
            kwargs={
                'day': today['day'],
                'month': today['month'],
                'year': today['year'],
            }
        ))

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
        days[date_human]['parloirs'] = {}

        # RETREATS:
        retreats = Retreat.objects.filter(
            date_from__lte=date)
        length_to_subtract_du = 2
        for index, retreat in enumerate(retreats):
            retreat_au = retreat.date_to()
            if retreat_au > initial_date_human:
                # Arrows:
                arrow_left = retreat.date_from < initial_date_human
                arrow_right = retreat_au > (
                    initial_date_human + datetime.timedelta(days=6))

                # Length and coord_x:
                # Max length allowed to the bar:
                max_length = 21 if (retreat.date_from < date_human) \
                    else (7 - i) * 3

                if retreat.date_from == date_human:
                    length = (((retreat_au - date_human).days) * 3)
                    coord_x = (i * 3) + 1 + length_to_subtract_du
                elif (retreat.date_from < date_human) \
                        and (retreat_au > (date_human + datetime.timedelta(days=7))) \
                        and (i == 0):
                    length = 21
                    coord_x = 1
                elif (retreat_au == date_human) \
                        and (retreat.date_from < initial_date_human):
                    length = (((date_human - initial_date_human).days) * 3) + 2
                    coord_x = 1
                else:
                    length = 0

                if length >= max_length:
                    length = max_length

                days[date_human]['retreats'][retreat] = {
                    'x': coord_x,
                    'length': length,
                    'arrow_left': arrow_left,
                    'arrow_right': arrow_right,
                }

        # SEJOURS:
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

            # Warnings about mails and oratory:
            warning_pere_suiveur = warning_sacristie = warning_oratoire = False
            if (sejour.personne.pere_suiveur is not None) and (not sejour.mail_pere_suiveur):
                warning_pere_suiveur = True
            if pretre and not sejour.mail_sacristie:
                warning_sacristie = True
            if pretre and not (sejour.oratoire or sejour.oratoire != ''):
                warning_oratoire = True

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
                'warning_oratoire': warning_oratoire,
            }

        # PARLOIRS:
        parloirs = Parloir.objects.filter(date=date).order_by('-date')
        for index, parloir in enumerate(parloirs):
            days[date_human]['parloirs'][parloir] = {
                'x': (i * 3) + 1,
                'length': 3,
            }

    return render(request, 'main/calendar.html', {
        'today': today,
        'days': days,
        'lines': range(21),
        'bold_lines': [2, 5, 8, 11, 14, 17, 20],
    })
