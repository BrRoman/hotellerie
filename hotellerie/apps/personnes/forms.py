""" apps/personnes/forms.py """

from django import forms

from .models import Personne


class PersonneForm(forms.ModelForm):
    """ Form for Personne. """
    class Meta:
        model = Personne
        fields = ['nom', 'prenom']
