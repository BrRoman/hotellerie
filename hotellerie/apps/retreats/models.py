""" apps/retreats/.models.py """

import datetime

from django.db import models


class Retreat(models.Model):
    """ Retreat model. """
    date_from = models.DateField()
    duration = models.IntegerField()

    def date_to(self):
        """ Returns the date_to of a retreat. """
        return self.date_from + datetime.timedelta(days=self.duration - 1)

    def date_to_string(self):
        """ Returns the date_to as a string of a retreat. """
        return self.date_to().strftime('%d/%m/%Y')

    def __str__(self):
        return 'Retraite du {} au {}'.format(
            self.date_from.strftime('%d/%m/%Y'),
            self.date_to_string()
        )
