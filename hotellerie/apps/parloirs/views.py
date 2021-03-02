""" apps/parloirs/views.py """


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth.decorators import login_required

from .forms import ParloirForm
from .models import Parloir


@login_required
def list(request):
    """ List of Parloirs. """
    parloirs = Parloir.objects.all().order_by('-date')
    return render(request, 'parloirs/list.html', {'parloirs': parloirs})


@login_required
def create(request):
    """ Create a Parloir. """
    if request.method == 'POST':
        form = ParloirForm(request.POST)
        if form.is_valid():
            form.save()
            date = form.cleaned_data['date']
            return HttpResponseRedirect(reverse('main:calendar', kwargs={
                'day': '{:%d}'.format(date),
                'month': '{:%m}'.format(date),
                'year': '{:%Y}'.format(date),
            }))

    else:
        form = ParloirForm()

    return render(request, 'parloirs/form.html', {'form': form})


@login_required
def details(request, *args, **kwargs):
    """ Details of a Parloir. """
    parloir = get_object_or_404(Parloir, id=kwargs['pk'])

    return render(request, 'parloirs/details.html', {
        'parloir': parloir,
        'calendar_day': parloir.date.strftime('%d'),
        'calendar_month': parloir.date.strftime('%m'),
        'calendar_year': parloir.date.strftime('%Y')
    })


@login_required
def update(request, *args, **kwargs):
    """ Update a Parloir. """
    parloir = get_object_or_404(Parloir, pk=kwargs['pk'])

    if request.method == 'POST':
        form = ParloirForm(request.POST, instance=parloir)
        if form.is_valid():
            form.save()
            date = form.cleaned_data['date']
            return HttpResponseRedirect(reverse('main:calendar', kwargs={
                'day': '{:%d}'.format(date),
                'month': '{:%m}'.format(date),
                'year': '{:%Y}'.format(date),
            }))
    else:
        form = ParloirForm(instance=parloir)

    return render(request, 'parloirs/form.html', {
        'form': form,
        'parloir': parloir,
    })


@login_required
def delete(request, *args, **kwargs):
    """ Delete a Parloir. """
    parloir = get_object_or_404(Parloir, pk=kwargs['pk'])

    if request.method == 'POST':
        form = ParloirForm(request.POST, instance=parloir)
        parloir.delete()
        return HttpResponseRedirect(reverse('main:calendar'))

    else:
        form = ParloirForm(instance=parloir)

    return render(request, 'parloirs/delete.html', {
        'form': form,
        'parloir': parloir,
    })
