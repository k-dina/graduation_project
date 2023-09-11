from .simulator.simulation import initialize_simulation, run_simulation
from .simulator.configuration import configure
from celery import shared_task



@shared_task()
def run_simulation_task(simulation_id, step):
    run_simulation(simulation_id, step)
