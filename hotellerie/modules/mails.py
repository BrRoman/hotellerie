""" Module mails. """

from django.core.mail import send_mail

from modules.dates import date_to_french_string
from modules.preferences import PREFERENCES

from apps.personnes.models import Mail, Personne


def mail_sacristie(sejour):
    """ Sends an email to sacristie and services. """
    priest = Personne.objects.get(pk=sejour.personne.pk)

    body = 'Mon cher Père,\n\n'
    body += 'Il va y avoir un prêtre-hôte :\n'
    body += '{}\n'.format(priest)
    body += 'Du : {}\n'.format(date_to_french_string(sejour.sejour_du))
    body += 'Au : {}\n\n'.format(date_to_french_string(sejour.sejour_au))
    body += 'Messe le lendemain de son arrivée\n' \
        if sejour.messe_lendemain \
        else 'IL CÉLÉBRERA LA MESSE LE JOUR DE SON ARRIVÉE'
    body += 'Forme : {}\n'.format(priest.messe_forme)
    body += 'Langue : {}\n'.format(priest.messe_langue)
    body += 'Tour de Messe : {}\n'.format(sejour.tour_messe)
    body += 'Attribuer un servant svp.\n\n' if sejour.servant else ''
    body += 'Commentaire : {}\n\n'.format(
        sejour.commentaire_sacristie) \
        if sejour.commentaire_sacristie else ''
    body += 'Bien à vous.\n'
    body += 'P. Vianney Marie'

    send_mail(
        'MESSE : {}'.format(priest),
        body,
        PREFERENCES['mail_hotelier'],
        [
            PREFERENCES['mail_sacristain'],
            PREFERENCES['mail_services']
        ],
        fail_silently=False,
    )


def mail_pere_suiveur(sejour):
    """ Sends an email to the Père suiveur. """
    guest = Personne.objects.get(pk=sejour.personne.pk)

    body = 'Mon cher Père,\n\n'
    body += 'Veuillez prendre bonne note de l’arrivée de cet hôte :\n\n'
    body += '{}\n\n'.format(guest)
    body += 'Arrivée le : {} ({})\n'.format(
        date_to_french_string(sejour.sejour_du),
        sejour.repas_du if sejour.repas_du != '---------' else 'repas non précisé'
    )
    body += 'Départ le : {} ({})\n'.format(
        date_to_french_string(sejour.sejour_au),
        sejour.repas_au if sejour.repas_au != '---------' else 'repas non précisé'
    )
    body += 'Chambre(s) : {}\n\n'.format(sejour.chambres_string())
    body += 'Je m’occupe de l’accueillir.\n\n'
    body += 'Bien à vous.\n'
    body += 'Père Vianney Marie'

    send_mail(
        'HÔTE : {}'.format(guest),
        body,
        PREFERENCES['mail_hotelier'],
        [', '.join(
            [str(mail)
             for mail in Mail.objects.filter(personne=guest.pere_suiveur)]
        )],
        fail_silently=False,
    )
