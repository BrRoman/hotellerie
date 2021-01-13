""" apps/parloirs/models.py """

from django.db import models

from apps.personnes.models import Personne


class Parloir(models.Model):
    """ Parloir model. """
    personne_1 = models.ForeignKey(
        to=Personne,
        on_delete=models.CASCADE,
        related_name='parloir_personne_1',
    )
    personne_2 = models.ForeignKey(
        null=True,
        to=Personne,
        on_delete=models.CASCADE,
        related_name='parloir_personne_2',
    )
    personne_3 = models.ForeignKey(
        null=True,
        to=Personne,
        on_delete=models.CASCADE,
        related_name='parloir_personne_3',
    )
    date = models.DateField()
    REPAS_NAMES = [
        ('Non défini', '---------'),
        ('Petit déjeuner', 'Petit déjeuner'),
        ('Déjeuner', 'Déjeuner'),
        ('Dîner', 'Dîner'),
    ]
    repas = models.CharField(
        max_length=50,
        choices=REPAS_NAMES,
    )
    nombre = models.IntegerField()
    PARLOIRS_NAMES = [
        ('Non défini', '---------'),
        ('Saint-Benoît', 'Saint-Benoît'),
        ('Saint-Ignace', 'Saint-Ignace'),
        ('Saint-Dominique', 'Saint-Dominique'),
        ('Parloir 1 vélux', 'Parloir 1 vélux'),
        ('Parloir 2 vélux', 'Parloir 2 vélux'),
        ('Salle de projection', 'Projection'),
    ]
    parloir = models.CharField(
        max_length=50,
        choices=PARLOIRS_NAMES,
    )
    repas_apporte = models.BooleanField(
        default=False,
    )
    remarque = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    last_modified = models.DateTimeField(
        auto_now=True,
    )

    def moines_string(self):
        """ Returns the monks concerned by the parloir as a string. """
        moines = self.personne_1.__str__()
        moines += ' + ' + self.personne_2.__str__() if self.personne_2 else ''
        moines += ' + ' + self.personne_3.__str__() if self.personne_3 else ''
        return moines

    def __str__(self):
        return "{} le {}".format(
            self.moines_string(),
            self.date.strftime('%d/%m/%Y'),
        )
