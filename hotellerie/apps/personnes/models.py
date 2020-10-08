""" apps/personnes.models.py """

import re

from django.db import models


class Personne(models.Model):
    """ Personne model. """
    nom = models.CharField(
        max_length=255,
    )
    prenom = models.CharField(
        max_length=255,
    )
    moine_flav = models.BooleanField(
        default=False,
    )
    est_pere_suiveur = models.BooleanField(
        default=False,
    )
    qualite = models.CharField(
        max_length=25,
    )
    pere_suiveur = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        db_column='pere_suiveur',
    )
    pretre = models.BooleanField(
        default=False,
    )
    messe_forme = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
    messe_langue = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
    commentaire = models.TextField()
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
        db_table = 'Personnes'

    def __str__(self):
        nom_complet = self.qualite
        nom_complet += ' ' if self.qualite else ''
        nom_complet += self.prenom if self.prenom else ''
        nom_complet += ' ' if self.prenom else ''
        name = re.sub(
            r'^DE ',
            lambda match: 'de ',
            self.nom.upper()
        )
        name = re.sub(
            r'^D\'',
            lambda match: 'd\'',
            self.nom.upper()
        )
        nom_complet += name
        return nom_complet


class Mail(models.Model):
    """ Mail model. """
    personne = models.ForeignKey(
        to='Personne',
        on_delete=models.CASCADE,
        db_column='id_personne',
        related_name='mail_personne',
    )
    mail = models.EmailField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='creation',
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        db_column='last_update',
    )

    class Meta:
        managed = False
        db_table = 'Mails'

    def __str__(self):
        return self.mail


class Telephone(models.Model):
    """ Telephone model. """
    personne = models.ForeignKey(
        to='Personne',
        on_delete=models.CASCADE,
        db_column='id_personne',
        related_name='tel_personne',
    )
    num_tel = models.CharField(
        max_length=25,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='creation',
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        db_column='last_update',
    )

    class Meta:
        managed = False
        db_table = 'Telephones'

    def __str__(self):
        return self.num_tel


class Adresse(models.Model):
    """ Adresse model. """
    personne = models.ForeignKey(
        to='Personne',
        on_delete=models.CASCADE,
        db_column='id_personne',
        related_name='adresse_personne',
    )
    rue = models.TextField()
    code_postal = models.CharField(
        max_length=25,
    )
    ville = models.CharField(
        max_length=50,
    )
    pays = models.CharField(
        max_length=25,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='creation',
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        db_column='last_update',
    )

    class Meta:
        managed = False
        db_table = 'Adresses'

    def __str__(self):
        adresse_as_string = ''
        adresse_as_string += self.rue + ' | ' if self.rue else ''
        adresse_as_string += self.code_postal + ' | ' if self.code_postal else ''
        adresse_as_string += self.ville + ' | ' if self.ville else ''
        return adresse_as_string
