""" apps/listings/views.py """

from django.shortcuts import render


def cuisine(request):
    """ Listing cuisine. """
    return render(request, 'listings/cuisine.html', {})


def hotellerie(request):
    """ Listing hotellerie. """
    return render(request, 'listings/hotellerie.html', {})
