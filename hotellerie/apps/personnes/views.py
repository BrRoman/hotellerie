""" apps/personnes/views.py """

import re
from dal import autocomplete

from django.contrib.auth.decorators import login_required
from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import AdresseForm, MailForm, PersonneForm, TelephoneForm
from .models import Adresse, Mail, Personne, Telephone


@login_required
def list(request, letter, search=''):
    """ List of Personnes. """
    if letter == '-':
        personnes = Personne.objects.filter(nom='')
    elif (len(letter) == 1) and (re.fullmatch(r'[A-Z]', letter)):
        personnes = Personne.objects.filter(nom__istartswith=letter)

    try:
        personnes
    except NameError:
        raise Http404()

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
    mails_inline_formset = forms.inlineformset_factory(
        Personne,
        Mail,
        fields=('mail',),
        form=MailForm,
        can_delete=True,
        extra=1,
    )
    tels_inline_formset = forms.inlineformset_factory(
        Personne,
        Telephone,
        fields=('num_tel',),
        form=TelephoneForm,
        can_delete=True,
        extra=1,
    )
    adresses_inline_formset = forms.inlineformset_factory(
        Personne,
        Adresse,
        fields=('rue', 'code_postal', 'ville', 'pays',),
        form=AdresseForm,
        can_delete=True,
        extra=1,
    )

    if request.method == 'POST':
        form = PersonneForm(request.POST)
        mails_formset = mails_inline_formset(request.POST)
        tels_formset = tels_inline_formset(request.POST)
        adresses_formset = adresses_inline_formset(request.POST)

        if form.is_valid() \
                and mails_formset.is_valid() \
                and tels_formset.is_valid() \
                and adresses_formset.is_valid():
            letter = form.cleaned_data['nom'][0].upper()
            personne = form.save()

            for form_mail in mails_formset:
                if form_mail.cleaned_data.get('mail') \
                        and not form_mail.cleaned_data.get('DELETE'):
                    Mail.objects.create(
                        personne=personne,
                        mail=form_mail.cleaned_data.get('mail'),
                    )

            for form_tel in tels_formset:
                if form_tel.cleaned_data.get('num_tel') \
                        and not form_tel.cleaned_data.get('DELETE'):
                    Telephone.objects.create(
                        personne=personne,
                        num_tel=form_tel.cleaned_data.get('num_tel'),
                    )

            for form_adresse in adresses_formset:
                if form_adresse.cleaned_data.get('rue') \
                        or form_adresse.cleaned_data.get('code_postal')\
                        or form_adresse.cleaned_data.get('ville') \
                        or form_adresse.cleaned_data.get('pays'):
                    if not form_adresse.cleaned_data.get('DELETE'):
                        Adresse.objects.create(
                            personne=personne,
                            rue=form_adresse.cleaned_data.get('rue'),
                            code_postal=form_adresse.cleaned_data.get(
                                'code_postal'),
                            ville=form_adresse.cleaned_data.get('ville'),
                            pays=form_adresse.cleaned_data.get('pays'),
                        )
            return HttpResponseRedirect(reverse(
                'personnes:list',
                args=letter
            ))

    else:
        form = PersonneForm()
        mails_formset = mails_inline_formset()
        tels_formset = tels_inline_formset()
        adresses_formset = adresses_inline_formset()

    return render(request, 'personnes/form.html', {
        'form': form,
        'mails_formset': mails_formset,
        'tels_formset': tels_formset,
        'adresses_formset': adresses_formset,
    })


@login_required
def details(request, **kwargs):
    """ Details of a Personne. """
    personne = get_object_or_404(Personne, pk=kwargs['pk'])
    first_letter = personne.nom[0] if personne.nom else '-'
    return render(request, 'personnes/details.html', {
        'personne': personne,
        'first_letter': first_letter,
        'mails': Mail.objects.filter(personne=personne),
        'tels': Telephone.objects.filter(personne=personne),
        'adresses': Adresse.objects.filter(personne=personne),
    })


@login_required
def update(request, **kwargs):
    """ Update a Personne. """
    personne = get_object_or_404(Personne, pk=kwargs['pk'])
    first_letter = personne.nom[0] if personne.nom else '-'
    mails_inline_formset = forms.inlineformset_factory(
        Personne,
        Mail,
        fields=('mail',),
        form=MailForm,
        can_delete=True,
        extra=1,
    )
    tels_inline_formset = forms.inlineformset_factory(
        Personne,
        Telephone,
        fields=('num_tel',),
        form=TelephoneForm,
        can_delete=True,
        extra=1,
    )
    adresses_inline_formset = forms.inlineformset_factory(
        Personne,
        Adresse,
        fields=('rue', 'code_postal', 'ville', 'pays',),
        form=AdresseForm,
        can_delete=True,
        extra=1,
    )

    if request.method == 'POST':
        form = PersonneForm(request.POST, instance=personne)
        mails_formset = mails_inline_formset(
            request.POST, instance=personne
        )
        tels_formset = tels_inline_formset(
            request.POST, instance=personne
        )
        adresses_formset = adresses_inline_formset(
            request.POST, instance=personne
        )

        if form.is_valid() \
                and mails_formset.is_valid() \
                and tels_formset.is_valid() \
                and adresses_formset.is_valid():
            form.save()
            Mail.objects.filter(personne=personne).delete()
            Telephone.objects.filter(personne=personne).delete()
            Adresse.objects.filter(personne=personne).delete()

            for form_mail in mails_formset:
                if form_mail.cleaned_data.get('mail') \
                        and not form_mail.cleaned_data.get('DELETE'):
                    Mail.objects.create(
                        personne=personne,
                        mail=form_mail.cleaned_data.get('mail'),
                    )

            for form_tel in tels_formset:
                if form_tel.cleaned_data.get('num_tel') \
                        and not form_tel.cleaned_data.get('DELETE'):
                    Telephone.objects.create(
                        personne=personne,
                        num_tel=form_tel.cleaned_data.get('num_tel'),
                    )

            for form_adresse in adresses_formset:
                if form_adresse.cleaned_data.get('rue') \
                        or form_adresse.cleaned_data.get('code_postal')\
                        or form_adresse.cleaned_data.get('ville') \
                        or form_adresse.cleaned_data.get('pays'):
                    if not form_adresse.cleaned_data.get('DELETE'):
                        Adresse.objects.create(
                            personne=personne,
                            rue=form_adresse.cleaned_data.get('rue'),
                            code_postal=form_adresse.cleaned_data.get(
                                'code_postal'),
                            ville=form_adresse.cleaned_data.get('ville'),
                            pays=form_adresse.cleaned_data.get('pays'),
                        )

            return HttpResponseRedirect(reverse(
                'personnes:details',
                kwargs={'pk': personne.id}
            ))

    else:
        form = PersonneForm(
            instance=personne,
        )
        mails_formset = mails_inline_formset(
            instance=personne
        )
        tels_formset = tels_inline_formset(
            instance=personne
        )
        adresses_formset = adresses_inline_formset(
            instance=personne
        )

    return render(request, 'personnes/form.html', {
        'form': form,
        'personne': personne,
        'first_letter': first_letter,
        'mails_formset': mails_formset,
        'tels_formset': tels_formset,
        'adresses_formset': adresses_formset,
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
            personnes = (personnes.filter(nom__icontains=self.q) |
                         personnes.filter(prenom__icontains=self.q))
        return personnes
