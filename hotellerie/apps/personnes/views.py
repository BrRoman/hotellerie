""" apps/personnes/views.py """

from dal import autocomplete

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import PersonneForm
from .models import Personne


@login_required
def home(request):
    """ Home view of Personnes. """
    return render(request, 'personnes/home.html', {})


@login_required
def list(request, letter, search=''):
    """ List of Personnes. """
    if letter == '-':
        personnes = Personne.objects.filter(nom='')
    else:
        personnes = Personne.objects.filter(nom__istartswith=letter)

    if request.method == 'POST':
        search = request.POST['filter']

    if search != '':
        personnes = (personnes.filter(nom__icontains=search) |
                     personnes.filter(prenom__icontains=search))

    personnes = personnes.order_by('nom')

    return render(request, 'personnes/list.html', {
        'letters': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '-'],
        'personnes': personnes,
        'current': letter,
        'filter': search,
    })


@login_required
def create(request):
    """ Create a Personne. """
    if request.method == 'POST':
        form = PersonneForm(request.POST)
        if form.is_valid():
            letter = form.cleaned_data['nom'][0].upper()
            form.save()
            return HttpResponseRedirect(reverse('personnes:list', args=letter))

    else:
        form = PersonneForm()

    return render(request, 'personnes/form.html', {'form': form})


@login_required
def details(request, **kwargs):
    """ Details of a Personne. """
    personne = get_object_or_404(Personne, pk=kwargs['pk'])
    first_letter = personne.nom[0] if personne.nom else '-'
    return render(request, 'personnes/details.html', {
        'personne': personne,
        'first_letter': first_letter
    })


@login_required
def update(request, **kwargs):
    """ Update a Personne. """
    personne = get_object_or_404(Personne, pk=kwargs['pk'])
    first_letter = personne.nom[0] if personne.nom else '-'

    if request.method == 'POST':
        form = PersonneForm(request.POST, instance=personne)
        if form.is_valid():
            letter = form.cleaned_data['nom'][0].upper()
            form.save()
            return HttpResponseRedirect(reverse('personnes:list', args=letter))

    else:
        form = PersonneForm(
            instance=personne,
        )

    return render(request, 'personnes/form.html', {
        'form': form,
        'personne': personne,
        'first_letter': first_letter
    })


@login_required
def delete(request, **kwargs):
    """ Delete a Personne. """
    personne = get_object_or_404(Personne, pk=kwargs['pk'])
    first_letter = personne.nom[0] if personne.nom else '-'

    if request.method == 'POST':
        form = PersonneForm(request.POST, instance=personne)
        personne.delete()
        return HttpResponseRedirect(reverse('personnes:list', args=first_letter))

    else:
        form = PersonneForm(instance=personne)

    return render(request, 'personnes/delete.html', {
        'form': form,
        'personne': personne,
        'first_letter': first_letter
    })


class PersonneAutocompleteView(autocomplete.Select2QuerySetView):
    """ Return a set of Personnes according to the user search value. """

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Personne.objects.none()

        personnes = Personne.objects.all()
        if self.q:
            personnes = personnes.filter(nom__istartswith=self.q)
        return personnes
