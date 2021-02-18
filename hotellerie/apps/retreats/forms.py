""" apps/personnes/forms.py """

from django import forms

from tempus_dominus.widgets import DatePicker

from .models import Retreat


class RetreatForm(forms.ModelForm):
    """ Form for Personnes. """
    date_from = forms.DateField(
        label='Date :',
        input_formats=[
            '%d/%m/%Y',
        ],
        widget=DatePicker(options={
            'format': 'DD/MM/YYYY',
        }),
    )
    duration = forms.IntegerField(
        label='Durée :',
        label_suffix='',
        initial=5,
    )

    class Meta:
        model = Retreat
        fields = ['date_from', 'duration']
