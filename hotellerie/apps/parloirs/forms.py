""" apps/parloirs/forms.py """

from django import forms

from .models import Parloir


class ParloirForm(forms.ModelForm):
    """ Form for Parloir. """
    class Meta:
        model = Parloir
        fields = ['date', 'parloir']
