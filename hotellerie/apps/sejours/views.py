""" apps/sejours/views.py """

from django.shortcuts import render
from django.views.generic import TemplateView


class SejoursHomeView(TemplateView):
    """ Home view of Sejours. """
    template_name = 'sejours/home.html'
