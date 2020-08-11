""" apps/sejours/forms.py """

from django import forms

from .models import Sejour


class SejourForm(forms.ModelForm):
    """ Form for Sejour. """
    class Meta:
        model = Sejour
        fields = ['sejour_du', 'repas_du', 'sejour_au', 'repas_au']
