""" apps/sejours/models.py """

from django.db import models

from apps.personnes.models import Personne


class Sejour(models.Model):
    """ Sejour class. """
    personne = models.ForeignKey(
        to=Personne,
        on_delete=models.CASCADE,
        db_column='id_personne',
    )
    sejour_du = models.DateField()
    sejour_au = models.DateField()
    repas_du = models.CharField(
        max_length=25,
    )
    repas_au = models.CharField(
        max_length=25,
    )
    mensa = models.CharField(
        max_length=25,
    )
    dit_messe = models.BooleanField(
        default=False,
    )
    messe_lendemain = models.BooleanField(
        default=False,
    )
    tour_messe = models.CharField(
        max_length=25,
    )
    servant = models.BooleanField(
        default=False,
    )
    commentaire_cuisine = models.TextField()
    commentaire_sacristie = models.TextField()
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
        db_table = 'Sejours'

    def __str__(self):
        return 'Séjour de {} du {} au {}'.format(
            self.personne,
            self.sejour_du.strftime('%d/%m/%Y'),
            self.sejour_au.strftime('%d/%m/%Y') if self.sejour_au else '--'
        )


class Chambre(models.Model):
    """ Chambre model. """
    sejour = models.ForeignKey(
        to='Sejour',
        on_delete=models.CASCADE,
        db_column='id_sejour',
    )
    chambre = models.CharField(
        max_length=25,
    )

    class Meta:
        managed = False
        db_table = 'Chambres'

    def __str__(self):
        return '{} ({})'.format(self.chambre, self.sejour.__str__())
