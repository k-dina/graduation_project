from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from mongoengine import connect

from .forms import SimulationForm, NameSimulationForm
from .tasks import run_simulation_task
from .simulator.simulation import initialize_simulation
from .simulator.configuration import *
from .simulator.models import Snapshot
from .simulator.mongo_db import drop_simulation, name_simulation, save_simulation, list_simulations, rename_simulation, delete_details, get_simulation_name


import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

connect('simulations', host='mongo', port=27017)


def get_user_name(user) -> str:
    return f'{user.username}'


def index(request):
    if request.user.is_authenticated:
        return redirect('userspace')
    return render(request, 'index.html')


def userspace(request):
    user = request.user
    context = {
        'user_name': get_user_name(user),
    }
    return render(request, 'userspace.html', context=context)


def newsimulation(request):
    next_page = None
    errors = None

    if request.method == 'GET':
        next_page = request.GET.get('next')
        form = SimulationForm()

    elif request.method == 'POST':
        form = SimulationForm(request.POST)

        if form.is_valid():
            configuration = configure(form.cleaned_data)
            simulation_id = initialize_simulation(configuration)
            run_simulation_task.apply_async(args=[simulation_id, 0])
            return HttpResponseRedirect(f'/view_simulation/{simulation_id}/')

        errors = 'The parameters are not filled or filled incorrectly! ' \
                 'Read the instructions carefully and resubmit the form'

    else:
        form = SimulationForm()

    return render(request, 'newsimulation.html', {'form': form, 'next': next_page, 'errors': errors})


def get_snapshots(request, id, step):
    new_data = Snapshot.objects(simulation_id=id, step__gte=step).order_by('step').limit(5)

    data = {}
    for snapshot in new_data:
        data[snapshot.step] = len(snapshot.blobs)

    return JsonResponse(data, status=200)


def resume_simulation(request, id, step):
    task = run_simulation_task.apply_async(args=[id, step - 1])
    return JsonResponse({'new_task_id': task.id}, status=200)


def view_simulation(request, id):
    last_step = len(Snapshot.objects(simulation_id=id))
    return render(request, 'view_simulation.html',
                  {'simulation_id': id, 'last_step': last_step})


def view_saved_simulation(request, simulation_id):
    last_step = 0
    return render(request, 'view_saved_simulation.html',
                  {'simulation_id': simulation_id, 'last_step': last_step})


def drop_simulation_view(request, simulation_id, next_page='simulations'):
    drop_simulation(simulation_id)
    user = request.user
    if user.is_authenticated:
        delete_details(simulation_id, user.id)
        next_page = 'saved_simulations'
    return redirect(next_page)



@login_required
def save_simulation_view(request, simulation_id):
    user_id = request.user.id

    save_simulation(user_id, simulation_id)

    return render(request, 'name_simulation.html', context={'simulation_id': simulation_id})


def name_simulation_view(request):
    errors = {}
    form = NameSimulationForm()

    if request.method == 'POST':
        form = NameSimulationForm(request.POST)
        if form.is_valid():
            simulation_id = form.cleaned_data['simulation_id']
            name = form.cleaned_data['name']
            name_simulation(simulation_id, name)
            return redirect('userspace')

        errors = form.errors
    return render(request, 'name_simulation.html', context={'form': form, 'errors': errors})


def saved_simulations(request):
    user_id = request.user.id
    simulation_names = list_simulations(user_id)

    return render(request, 'saved_simulations.html', context={'simulation_names': simulation_names})


def options_view(request, simulation_id):
    return render(request, 'options.html', context={'simulation_id': simulation_id, 'simulation_name': get_simulation_name(simulation_id)})


def rename_simulation_view(request, simulation_id):
    errors = {}
    form = NameSimulationForm()

    if request.method == 'POST':
        form = NameSimulationForm(request.POST)
        if form.is_valid():
            simulation_id = form.cleaned_data['simulation_id']
            name = form.cleaned_data['name']
            rename_simulation(simulation_id, name)
            return redirect('saved_simulations')

        errors = form.errors
    return render(request, 'rename_simulation.html', context={'form': form, 'errors': errors, 'new': 'new', 'simulation_id':simulation_id})


