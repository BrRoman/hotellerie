""" apps/sejours/forms.py """

from dal import autocomplete

from django import forms
from tempus_dominus.widgets import DatePicker

from apps.personnes.models import Personne
from .models import Sejour


class SejourForm(forms.ModelForm):
    """ Form for Sejour. """
    personne = forms.ModelChoiceField(
        label='Personne :',
        error_messages={
            'required': 'Ce champ est obligatoire',
        },
        queryset=Personne.objects.all(),
        widget=autocomplete.ModelSelect2(url='personnes:autocomplete'),
    )
    sejour_du = forms.DateField(
        label='Du :',
        input_formats=[
            '%d/%m/%Y',
        ],
        widget=DatePicker(options={
            'format': 'DD/MM/YYYY',
        }),
    )
    sejour_au = forms.DateField(
        label='Au :',
        required=False,
        input_formats=[
            '%d/%m/%Y',
        ],
        widget=DatePicker(options={
            'format': 'DD/MM/YYYY',
        }),
    )
    repas_du = forms.ChoiceField(
        choices=[
            ('---------', ''),
            ('Petit-déjeuner', 'Petit-déjeuner'),
            ('Déjeuner', 'Déjeuner'),
            ('Dîner', 'Diner'),
        ],
    )
    repas_au = forms.ChoiceField(
        required=False,
        choices=[
            ('---------', ''),
            ('Petit-déjeuner', 'Petit-déjeuner'),
            ('Déjeuner', 'Déjeuner'),
            ('Dîner', 'Diner'),
        ],
    )
    mensa = forms.ChoiceField(
        label="Table",
        choices=[
            ('Sans repas', 'Sans repas'),
            ('Hôtes', 'Table des hôtes'),
            ('Table abbatiale', 'Table abbatiale'),
            ('Moines', 'Table des moines'),
        ],
    )
    dit_messe = forms.BooleanField(
        label='Prêtre avec Messe',
        label_suffix='',
        required=False,
    )
    messe_lendemain = forms.BooleanField(
        label='Aura dit la Messe à son arrivée',
        label_suffix='',
        required=False,
    )
    tour_messe = forms.ChoiceField(
        label='Tour de Messe :',
        required=False,
        choices=[
            ('---------', ''),
            ('1er tour', '1er tour'),
            ('2e tour', '2e tour'),
            ('Matinée', 'Matinée'),
        ]
    )
    servant = forms.BooleanField(
        label='Attribuer un servant',
        label_suffix='',
        required=False,
    )
    commentaire_cuisine = forms.CharField(
        required=False,
        label='Remarques pour la cuisine :',
        widget=forms.Textarea(
            attrs={
                'rows': 4,
            }
        ),
    )
    commentaire_sacristie = forms.CharField(
        required=False,
        label='Remarques pour la sacristie :',
        widget=forms.Textarea(
            attrs={
                'rows': 4,
            }
        ),
    )

    class Meta:
        model = Sejour
        fields = ('__all__')
