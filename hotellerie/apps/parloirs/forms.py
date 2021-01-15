""" apps/parloirs/forms.py """

from dal import autocomplete

from django import forms
from tempus_dominus.widgets import DatePicker

from apps.personnes.models import Personne
from .models import Parloir


class ParloirForm(forms.ModelForm):
    """ Form for Parloirs. """
    personne_1 = forms.ModelChoiceField(
        label='Moine 1 :',
        error_messages={
            'required': 'Ce champ est obligatoire',
        },
        queryset=Personne.objects.all(),
        widget=autocomplete.ModelSelect2(url='personnes:autocomplete_monks'),
    )
    personne_2 = forms.ModelChoiceField(
        label='Moine 2 :',
        required=False,
        queryset=Personne.objects.all(),
        widget=autocomplete.ModelSelect2(url='personnes:autocomplete_monks'),
    )
    personne_3 = forms.ModelChoiceField(
        label='Moine 3 :',
        required=False,
        queryset=Personne.objects.all(),
        widget=autocomplete.ModelSelect2(url='personnes:autocomplete_monks'),
    )
    date = forms.DateField(
        label='Date :',
        input_formats=[
            '%d/%m/%Y',
        ],
        widget=DatePicker(options={
            'format': 'DD/MM/YYYY',
        }),
    )
    repas = forms.ChoiceField(
        choices=[
            ('Non défini', '---------'),
            ('Petit déjeuner', 'Petit déjeuner'),
            ('Déjeuner', 'Déjeuner'),
            ('Dîner', 'Dîner'),
        ],
    )
    nombre = forms.IntegerField(
        help_text="Nombre de personnes en plus des personnes ci-dessus",
    )
    parloir = forms.ChoiceField(
        label="Parloir :",
        choices=[
            ('Non défini', '---------'),
            ('Saint-Benoît', 'Saint-Benoît'),
            ('Saint-Ignace', 'Saint-Ignace'),
            ('Saint-Dominique', 'Saint-Dominique'),
            ('Parloir 1 vélux', 'Parloir 1 vélux'),
            ('Parloir 2 vélux', 'Parloir 2 vélux'),
            ('Salle de projection', 'Projection'),
        ],
    )
    repas_apporte = forms.BooleanField(
        required=False,
        label='Repas apporté',
        label_suffix='',
    )
    remarque = forms.CharField(
        required=False,
        label='Remarques :',
        widget=forms.Textarea,
    )

    class Meta:
        model = Parloir
        fields = ('__all__')
