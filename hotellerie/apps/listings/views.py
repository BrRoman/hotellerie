""" apps/listings/views.py """

from datetime import date, timedelta
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from django.http import FileResponse
from django.shortcuts import render

from modules.dates import date_to_french_string
from apps.sejours.models import Sejour


def cuisine(request):
    """ Listing cuisine. """
    days = {}
    today = date.today()
    for i in range(15):
        day = today + timedelta(days=i)
        day_string = date_to_french_string(day)

        # Midi:
        table_hotes_midi = []
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
            table_hotes_midi.append({
                'hote': hote,
                'is_first_repas': is_first_repas,
                'is_last_repas': is_last_repas,
                'is_monorepas': is_monorepas,
            })

        # Soir:

        days[day] = {
            'day_string': day_string,
            'midi': {
                'table_hotes': table_hotes_midi,
                # 'table_moines': moines_midi,
                # 'table_abbatiale': abbatiale_midi,
            },
            # 'soir': {
            #     'table_hotes': hotes_soir,
            #     'table_moines': moines_soir,
            #     'table_abbatiale': abbatiale_soir,
            # },
        }
    return render(request, 'listings/cuisine.html', {'days': days})


def hotellerie(request):
    """ Listing hotellerie. """
    buffer = io.BytesIO()
    # Settings:
    width, height = A4
    pdf = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
    pdf.setFont("Helvetica", 10)
    pdf.saveState()
    pdf.setLineWidth(0.2)

    pdf.drawString(100, 100, "Listing hôtellerie")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, filename='listing_hotellerie.pdf')
