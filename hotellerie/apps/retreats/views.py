""" apps/retreats/views.py """


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse


from .forms import RetreatForm
from .models import Retreat


@login_required
def list(request):
    """ List of retreats. """
    retreats = Retreat.objects.all().order_by('-date_from')
    return render(
        request,
        'retreats/list.html',
        {
            'retreats': retreats,
        }
    )


@login_required
def create(request):
    """ Create a Retreat. """
    if request.method == 'POST':
        form = RetreatForm(request.POST)

        if form.is_valid():
            form.save()
            date = form.cleaned_data['date_from']
            return HttpResponseRedirect(reverse('main:calendar', kwargs={
                'day': '{:%d}'.format(date),
                'month': '{:%m}'.format(date),
                'year': '{:%Y}'.format(date),
            }))

    else:
        form = RetreatForm()

    return render(request, 'retreats/form.html', {'form': form})


@login_required
def details(request, *args, **kwargs):
    """ Details of a Retreat. """
    retreat = get_object_or_404(Retreat, pk=kwargs['pk'])
    return render(request, 'retreats/details.html', {
        'retreat': retreat
    })


@login_required
def update(request, **kwargs):
    """ Update a Retreat. """
    retreat = get_object_or_404(Retreat, pk=kwargs['pk'])

    if request.method == 'POST':
        form = RetreatForm(request.POST, instance=retreat)

        if form.is_valid():
            form.save()
            date = form.cleaned_data['date_from']
            return HttpResponseRedirect(reverse('main:calendar', kwargs={
                'day': '{:%d}'.format(date),
                'month': '{:%m}'.format(date),
                'year': '{:%Y}'.format(date),
            }))

    else:
        form = RetreatForm(
            instance=retreat,
        )

    return render(request, 'retreats/form.html', {
        'form': form,
        'retreat': retreat,
    })


@login_required
def delete(request, **kwargs):
    """ Delete a Retreat. """
    retreat = get_object_or_404(Retreat, pk=kwargs['pk'])

    if request.method == 'POST':
        form = RetreatForm(request.POST, instance=retreat)
        retreat.delete()
        return HttpResponseRedirect(reverse('main:calendar'))

    form = RetreatForm(instance=retreat)

    return render(request, 'retreats/delete.html', {
        'form': form,
        'retreat': retreat,
    })
