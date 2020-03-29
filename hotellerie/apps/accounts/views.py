""" apps/accounts/views.py """

from django.contrib.auth.views import LoginView

from .forms import HotellerieLoginForm


class HotellerieLoginView(LoginView):
    """ Login view. """
    form_class = HotellerieLoginForm
    template_name = 'accounts/login.html'
