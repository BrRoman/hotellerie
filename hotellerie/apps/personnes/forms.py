""" apps/personnes/forms.py """

from django import forms

from .models import Personne
from apps.personnes.models import Personne


class PersonneForm(forms.ModelForm):
    """ Form for Personne. """
    qualite = forms.ChoiceField(
        label='Qualité :',
        choices=[
            ('Abbé', 'Abbé'),
            ('Abbés', 'Abbés'),
            ('Brother', 'Brother'),
            ('Capitaine', 'Capitaine'),
            ('Cardinal', 'Cardinal'),
            ('Chanoine', 'Chanoine'),
            ('Colonel', 'Colonel'),
            ('Commandant', 'Commandant'),
            ('Docteur', 'Docteur'),
            ('Dom', 'Dom'),
            ('Don', 'Don'),
            ('Famille', 'Famille'),
            ('Father', 'Father'),
            ('Frère', 'Frère'),
            ('Frères', 'Frères'),
            ('Général', 'Général'),
            ('Le Comte', 'Le Comte'),
            ('Le TRP Abbé', 'Le TRP Abbé'),
            ('M. l\'Abbé', 'M. l\'Abbé'),
            ('M. le chanoine', 'M. le chanoine'),
            ('M. l’Abbé', 'M. l’Abbé'),
            ('Madame', 'Madame'),
            ('Mademoiselle', 'Mademoiselle'),
            ('Mère', 'Mère'),
            ('Messieurs', 'Messieurs'),
            ('Monseigneur', 'Monseigneur'),
            ('Monsieur', 'Monsieur'),
            ('Monsieur et Madame', 'Monsieur et Madame'),
            ('Monsieur l’Abbé', 'Monsieur l’Abbé'),
            ('Père', 'Père'),
            ('Pères', 'Pères'),
            ('Princesse', 'Princesse'),
            ('Professeur', 'Professeur'),
            ('Rev. Father', 'Rev. Father'),
            ('Révérendes Mères', 'Révérendes Mères'),
            ('RP.', 'RP.'),
            ('Sig.', 'Sig.'),
            ('Soeur', 'Soeur'),
            ('Soeurs', 'Soeurs'),
            ('Sœur', 'Sœur'),
            ('Sœurs', 'Sœurs'),
            ('TR PERE', 'TR PERE'),
        ],
        error_messages={
            'required': 'Ce champ est obligatoire',
        },
    )
    nom = forms.CharField(
        required=False,
        label='Nom :',
        max_length=255,
        error_messages={
            'required': 'Ce champ est obligatoire.',
        },
    )
    prenom = forms.CharField(
        required=False,
        label='Prénom :',
        max_length=255,
        error_messages={
            'required': 'Ce champ est obligatoire.',
        },
    )
    moine_flav = forms.BooleanField(
        required=False,
        label='Est un moine de Flavigny',
        label_suffix=''
    )
    est_pere_suiveur = forms.BooleanField(
        required=False,
        label='Est un Père suiveur',
        label_suffix=''
    )
    pere_suiveur = forms.ModelChoiceField(
        required=False,
        queryset=Personne.objects.filter(
            est_pere_suiveur=True).order_by('prenom'),
        label='Père suiveur :',
    )
    pretre = forms.BooleanField(
        required=False,
        label='Est un prêtre',
        label_suffix='',
    )
    messe_forme = forms.ChoiceField(
        required=False,
        label='Messe - forme :',
        choices=[
            ('', '---------'),
            ('Ordinaire', 'Ordinaire'),
            ('Extraordinaire', 'Extraordinaire'),
        ],
    )
    messe_langue = forms.ChoiceField(
        required=False,
        label='Messe - langue :',
        choices=[
            ('', '---------'),
            ('Français', 'Français'),
            ('Latin', 'Latin'),
            ('Anglais', 'Anglais'),
            ('Allemand', 'Allemand'),
            ('Espagnol', 'Espagnol'),
            ('Néerlandais', 'Néerlandais'),
        ],
    )
    commentaire = forms.CharField(
        required=False,
        label='Remarques',
        widget=forms.Textarea,
    )

    class Meta:
        model = Personne
        fields = ['qualite', 'nom', 'prenom', 'commentaire',
                  'moine_flav', 'est_pere_suiveur', 'pere_suiveur', 'pretre', 'messe_forme', 'messe_langue']
