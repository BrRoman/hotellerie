""" Module dates """


def date_to_french_string(date):
    """ Converts a date into french format. """
    weekdays = ['Lundi', 'Mardi', 'Mercredi',
                'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
    weekday = weekdays[date.weekday()]
    day = date.day
    month = months[date.month - 1]
    return '{} {} {}'.format(weekday, day, month)
