""" apps/sejours/models.py """

from django.db import models

from apps.personnes.models import Personne


class Sejour(models.Model):
    """ Sejour class. """
    personne = models.ForeignKey(
        to=Personne,
        on_delete=models.CASCADE,
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
    mail_sacristie = models.BooleanField(
        default=False,
    )
    mail_pere_suiveur = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    last_modified = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return 'Séjour de {} du {} ({}) au {} ({})'.format(
            self.personne,
            self.sejour_du.strftime('%d/%m/%Y'),
            self.repas_du,
            self.sejour_au.strftime('%d/%m/%Y') if self.sejour_au else '--',
            self.repas_au
        )

    def chambres_string(self):
        """ Returns the rooms of the Sejour as a string. """
        chambres_queryset = Chambre.objects.filter(
            sejour=self).values('chambre')
        chambres_string = ''
        for chambre in chambres_queryset:
            chambres_string += (', ' if chambres_string !=
                                '' else '') + chambre['chambre']
        return chambres_string


class Chambre(models.Model):
    """ Chambre model. """
    sejour = models.ForeignKey(
        to='Sejour',
        on_delete=models.CASCADE,
    )
    chambre = models.CharField(
        max_length=25,
    )

    def __str__(self):
        return '{} ({})'.format(self.chambre, self.sejour.__str__())
