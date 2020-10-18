""" apps/listings/views.py """

from datetime import datetime, time, timedelta
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from django.http import FileResponse
from django.shortcuts import render

from modules.dates import date_to_french_string


def cuisine(request):
    """ Listing cuisine. """
    days = {}
    today = datetime.today()
    for i in range(15):
        date = date_to_french_string(today + timedelta(days=i))
        days[date] = {}
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
