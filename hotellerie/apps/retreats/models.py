""" apps/retreats/.models.py """

import datetime

from django.db import models


class Retreat(models.Model):
    """ Retreat model. """
    date_from = models.DateField()
    duration = models.IntegerField()

    def __str__(self):
        return 'Retraite du {}'.format(self.date_from)

    def date_to(self):
        """ Returns the date_to of a retreat. """
        return self.date_from + datetime.timedelta(days=self.duration)
