""" apps/listings/views.py """

from datetime import datetime, time, timedelta
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
    return render(request, 'listings/hotellerie.html', {})
