""" Module mails. """

from django.core.mail import send_mail

from modules.preferences import PREFERENCES

from apps.personnes.models import Personne


def mail_sacristie(sejour):
    """ Sends an email to sacristie and services. """
    priest = Personne.objects.get(pk=sejour.personne.pk)

    message = 'Mon cher Père,\n'
    message += 'Il va y avoir un prêtre-hôte :\n'
    message += '{}\n'.format(priest)
    message += ', du {} au {}\n'.format(sejour.sejour_du, sejour.sejour_au)

    send_mail(
        'Prêtre-hôte',
        message,
        PREFERENCES['mail_hotelier'],
        [
            PREFERENCES['mail_sacristain'],
            PREFERENCES['mail_services']
        ],
        fail_silently=False,
    )
