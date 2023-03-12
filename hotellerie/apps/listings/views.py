""" apps/listings/views.py """

import csv
from datetime import date, timedelta
import io
import os
import re

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from django.http import FileResponse
from django.conf import settings
from django.shortcuts import render

from modules.dates import date_to_french_string
from apps.parloirs.models import Parloir
from apps.sejours.models import Sejour

DAYS = {}
TODAY = date.today()


def cuisine(request):
    """ Listing cuisine. """
    for i in range(15):
        day = TODAY + timedelta(days=i)
        day_string = date_to_french_string(day)
        hote = is_first_repas = is_last_repas = is_monorepas = ''
        table_hotes_midi, \
            table_hotes_soir, \
            table_abbatiale_midi, \
            table_abbatiale_soir, \
            table_moines_midi, \
            table_moines_soir, \
            table_parloirs_midi, \
            table_parloirs_soir, \
            parloirs_midi, \
            parloirs_soir = (
                [] for i in range(10)
            )
        total_table_hotes_midi = \
            total_table_hotes_soir = \
            total_table_abbatiale_midi = \
            total_table_abbatiale_soir = \
            total_table_moines_midi = \
            total_table_moines_soir = \
            total_table_parloirs_midi = \
            total_table_parloirs_soir = \
            total_parloirs_midi = \
            total_parloirs_soir = 0

        # MIDI:
        sejours_midi = ((Sejour.objects.filter(
            sejour_du__lte=day
        ) & Sejour.objects.filter(
            sejour_au__gte=day
        )) | (Sejour.objects.filter(
            sejour_du__lte=day
        ) & Sejour.objects.filter(
            sejour_au=day
        )) | (Sejour.objects.filter(
            sejour_du=day
        ) & Sejour.objects.filter(
            sejour_au__gte=day
        ))).exclude(
            sejour_du=day, repas_du='Dîner'
        ).exclude(
            sejour_au=day, repas_au='Petit-déjeuner'
        )

        for index, sejour in enumerate(sejours_midi):
            hote = sejour.personne.__str__()
            nombre = len(sejour.chambres_string().split(', '))
            is_first_repas = (
                sejour.sejour_du == day
            ) and ((
                sejour.repas_du == 'Déjeuner'
            ) or (
                sejour.repas_du == 'Petit-déjeuner'
            ))
            is_last_repas = ((
                sejour.sejour_au == day
            ) and (
                sejour.repas_au == 'Déjeuner'
            ))
            is_monorepas = (
                sejour.sejour_du == sejour.sejour_au
            ) and (
                sejour.repas_du == sejour.repas_au
            )

            # Midi - tables hôtes:
            if sejour.mensa == 'Hôtes':
                total_table_hotes_midi += nombre
                table_hotes_midi.append({
                    'hote': hote,
                    'nombre': nombre,
                    'is_first_repas': is_first_repas,
                    'is_last_repas': is_last_repas,
                    'is_monorepas': is_monorepas,
                })

            # Midi - table abbatiale:
            if sejour.mensa == 'Table abbatiale':
                total_table_abbatiale_midi += nombre
                table_abbatiale_midi.append({
                    'hote': hote,
                    'nombre': nombre,
                    'is_first_repas': is_first_repas,
                    'is_last_repas': is_last_repas,
                    'is_monorepas': is_monorepas,
                })

            # Midi - table moines:
            if sejour.mensa == 'Moines':
                total_table_moines_midi += nombre
                table_moines_midi.append({
                    'hote': hote,
                    'nombre': nombre,
                    'is_first_repas': is_first_repas,
                    'is_last_repas': is_last_repas,
                    'is_monorepas': is_monorepas,
                })

            # Midi - repas aux parloirs:
            if sejour.mensa == 'Parloirs':
                total_table_parloirs_midi += nombre
                table_parloirs_midi.append({
                    'hote': hote,
                    'nombre': nombre,
                    'is_first_repas': is_first_repas,
                    'is_last_repas': is_last_repas,
                    'is_monorepas': is_monorepas,
                })

        # Midi: moines aux parloirs:
        parloirs_midi = Parloir.objects.filter(
            date=day
        ) & Parloir.objects.filter(
            repas='Déjeuner'
        )
        for index, parloir in enumerate(parloirs_midi):
            if not parloir.repas_apporte:
                total_parloirs_midi += (
                    parloir.nombre + 1 +
                    len(re.findall(' + ', parloir.moines_string()))
                )

        # SOIR:
        sejours_soir = ((Sejour.objects.filter(
            sejour_du__lte=day
        ) & Sejour.objects.filter(
            sejour_au__gte=day
        )) | (Sejour.objects.filter(
            sejour_du__lte=day
        ) & Sejour.objects.filter(
            sejour_au=day
        )) | (Sejour.objects.filter(
            sejour_du=day
        ) & Sejour.objects.filter(
            sejour_au__gte=day
        ))).exclude(
            sejour_au=day, repas_au='Petit-déjeuner'
        ).exclude(
            sejour_au=day, repas_au='Déjeuner'
        )

        for index, sejour in enumerate(sejours_soir):
            hote = sejour.personne.__str__()
            nombre = len(sejour.chambres_string().split(', '))
            is_first_repas = (
                sejour.sejour_du == day
            ) and (
                sejour.repas_du == 'Dîner'
            )
            is_last_repas = ((
                sejour.sejour_au == day
            ) and (
                sejour.repas_au == 'Dîner'
            )) or ((
                sejour.sejour_au == day + timedelta(days=1)
            ) and (
                sejour.repas_au == 'Petit-déjeuner'
            ))
            is_monorepas = (
                sejour.sejour_du == sejour.sejour_au
            ) and (
                sejour.repas_du == sejour.repas_au
            )

            # Soir - tables hôtes:
            if sejour.mensa == 'Hôtes':
                total_table_hotes_soir += nombre
                table_hotes_soir.append({
                    'hote': hote,
                    'nombre': nombre,
                    'is_first_repas': is_first_repas,
                    'is_last_repas': is_last_repas,
                    'is_monorepas': is_monorepas,
                })

            # Soir - table abbatiale:
            if sejour.mensa == 'Table abbatiale':
                total_table_abbatiale_soir += nombre
                table_abbatiale_soir.append({
                    'hote': hote,
                    'nombre': nombre,
                    'is_first_repas': is_first_repas,
                    'is_last_repas': is_last_repas,
                    'is_monorepas': is_monorepas,
                })

            # Soir - table moines:
            if sejour.mensa == 'Moines':
                total_table_moines_soir += nombre
                table_moines_soir.append({
                    'hote': hote,
                    'nombre': nombre,
                    'is_first_repas': is_first_repas,
                    'is_last_repas': is_last_repas,
                    'is_monorepas': is_monorepas,
                })

            # Soir - repas aux parloirs:
            if sejour.mensa == 'Parloirs':
                total_table_parloirs_soir += nombre
                table_parloirs_soir.append({
                    'hote': hote,
                    'nombre': nombre,
                    'is_first_repas': is_first_repas,
                    'is_last_repas': is_last_repas,
                    'is_monorepas': is_monorepas,
                })

        # Soir: moines aux parloirs:
        parloirs_soir = Parloir.objects.filter(
            date=day
        ) & Parloir.objects.filter(
            repas='Dîner'
        )
        for index, parloir in enumerate(parloirs_soir):
            if not parloir.repas_apporte:
                total_parloirs_soir += (
                    parloir.nombre + 1 +
                    len(re.findall(' + ', parloir.moines_string()))
                )

        # On compile le tout pour le jour concerné :
        DAYS[day] = {
            'day_string': day_string,
            'midi': {
                'table_hotes': table_hotes_midi,
                'total_table_hotes_midi': total_table_hotes_midi,
                'table_abbatiale': table_abbatiale_midi,
                'total_table_abbatiale_midi': total_table_abbatiale_midi,
                'table_moines': table_moines_midi,
                'total_table_moines_midi': total_table_moines_midi,
                'table_parloirs': table_parloirs_midi,
                'total_table_parloirs_midi': total_table_parloirs_midi,
                'parloirs': parloirs_midi,
                'total_parloirs_midi': total_parloirs_midi,
            },
            'soir': {
                'table_hotes': table_hotes_soir,
                'total_table_hotes_soir': total_table_hotes_soir,
                'table_abbatiale': table_abbatiale_soir,
                'total_table_abbatiale_soir': total_table_abbatiale_soir,
                'table_moines': table_moines_soir,
                'total_table_moines_soir': total_table_moines_soir,
                'table_parloirs': table_parloirs_soir,
                'total_table_parloirs_soir': total_table_parloirs_soir,
                'parloirs': parloirs_soir,
                'total_parloirs_soir': total_parloirs_soir,
            },
        }

    # Export in csv file:
    with open(os.path.join(settings.BASE_DIR, 'static/hospites.csv'), 'w', newline='') as csvfile:
        content = csv.writer(
            csvfile,
            delimiter=',',
            quoting=csv.QUOTE_MINIMAL,
        )
        content.writerow(
            [
                'Jour',
                'TH petit-déj.',
                'TH midi',
                'TH soir',
                'TM petit-déj.',
                'TM midi',
                'TM soir',
                '',
                '',
                '',
                'TP petit-déj.',
                'TP midi',
                'TP soir'
            ]
        )
        for index, day in enumerate(DAYS):
            content.writerow(
                [
                    DAYS[day]['day_string'],
                    '',
                    DAYS[day]['midi']['total_table_hotes_midi'],
                    DAYS[day]['soir']['total_table_hotes_soir'],
                    '',
                    DAYS[day]['midi']['total_table_moines_midi'],
                    DAYS[day]['soir']['total_table_moines_soir'],
                    '',
                    '',
                    '',
                    '',
                    DAYS[day]['midi']['total_table_parloirs_midi'],
                    DAYS[day]['soir']['total_table_parloirs_soir'],
                ]
            )

    return render(request, 'listings/cuisine.html', {'days': DAYS})


def hotellerie(request):
    """ Listing hotellerie. """
    buffer = io.BytesIO()
    # Settings:
    width, height = A4
    pdf = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
    pdf.setFont("Helvetica", 10)
    pdf.saveState()
    pdf.setLineWidth(0.2)

    # Title:
    coord_y = 50
    pdf.drawCentredString(width/2.0, coord_y, "+")
    coord_y += 15
    pdf.drawCentredString(width/2.0, coord_y, "PAX")
    coord_y += 15
    pdf.drawCentredString(width/2.0, coord_y, "LISTING HÔTELLERIE")

    # Parloirs:
    parloirs = Parloir.objects.filter(
        date__gte=TODAY
    ) & Parloir.objects.filter(
        date__lte=TODAY + timedelta(days=15)
    ).order_by('date')
    if parloirs:
        coord_y += 35
        pdf.drawCentredString(width/2.0, coord_y, "PARLOIRS")
        coord_y += 10
        for index, parloir in enumerate(parloirs):
            coord_y += 15
            line = ''
            line += '- {}'.format(
                date_to_french_string(parloir.date))
            line += ' ({})'.format(parloir.repas) if parloir.repas else ''
            line += ' : {}'.format(parloir.moines_string())
            line += ' + {}'.format(parloir.nombre) if parloir.nombre else ''
            line += ' (repas apporté)' if parloir.repas_apporte else ''
            pdf.drawString(40, coord_y, line)
            line = 'Parloir : {}'.format(
                parloir.parloir) if parloir.parloir and parloir.parloir != 'Non défini' else ''
            if line:
                coord_y += 15
                pdf.drawString(60, coord_y, line)

    # Hôtes:
    coord_y += 35
    pdf.drawCentredString(width/2.0, coord_y, "HÔTES")
    coord_y += 10
    sejours = ((Sejour.objects.filter(
        sejour_du__lte=TODAY
    ) & Sejour.objects.filter(
        sejour_au__gte=TODAY
    )) | (Sejour.objects.filter(
        sejour_du__lte=TODAY
    ) & Sejour.objects.filter(
        sejour_au=TODAY
    )) | (Sejour.objects.filter(
        sejour_du=TODAY
    ) & Sejour.objects.filter(
        sejour_au__gte=TODAY
    )) | (Sejour.objects.filter(
        sejour_du__gte=TODAY
    ) & Sejour.objects.filter(
        sejour_du__lte=TODAY + timedelta(days=15)
    ))).order_by('sejour_du', 'sejour_au')
    for index, sejour in enumerate(sejours):
        coord_y += 20
        line = ''
        line += '- {}'.format(sejour.personne.__str__())
        pdf.drawString(40, coord_y, line)
        coord_y += 13
        line = 'Du {} ({}) au {} ({})'.format(
            date_to_french_string(sejour.sejour_du),
            sejour.repas_du,
            date_to_french_string(sejour.sejour_au),
            sejour.repas_au,
        )
        pdf.drawString(60, coord_y, line)
        coord_y += 13
        line = 'Chambre(s) : {}'.format(sejour.chambres_string())
        pdf.drawString(60, coord_y, line)
        if sejour.dit_messe:
            coord_y += 13
            if sejour.oratoire:
                line = 'Oratoire : {} {}'.format(
                    sejour.oratoire,
                    sejour.tour_messe
                )
            else:
                line = 'Oratoire non défini.'
            pdf.drawString(60, coord_y, line)
        if coord_y > 800:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            coord_y = 0

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, filename='listing_hotellerie.pdf')
