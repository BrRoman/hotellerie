""" apps/parloirs/models.py """

from django.db import models

from apps.personnes.models import Personne


class Parloir(models.Model):
    """ Parloir model. """
    personne = models.ForeignKey(
        to=Personne,
        on_delete=models.CASCADE,
        db_column='id_personne',
    )
    date = models.DateField()
    nombre = models.IntegerField()
    PARLOIRS_NAMES = [
        ('Saint-Benoit', 'Saint-Benoit'),
        ('Saint-Ignace', 'Saint-Ignace'),
        ('Saint-Dominique', 'Saint-Dominique'),
    ]
    parloir = models.CharField(
        max_length=50,
        choices=PARLOIRS_NAMES,
    )
    remarque = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='created',
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        db_column='last_update',
    )

    class Meta:
        managed = False
        db_table = 'Parloirs'

    def __str__(self):
        return "{} le {}".format(self.personne, self.date)
