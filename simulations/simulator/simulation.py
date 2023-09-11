import random
import numpy as np
from .mongo_db import save_snapshot, save_configuration, get_snapshot_by_step, get_config, \
    restore_snapshot
from .processors.functions import clamp
import uuid

from .processors.field_processor import FieldProcessor
from .processors.health_speed_processor import HealthSpeedProcessor
from .processors.mating_processor import MatingProcessor
from .processors.harvesting_processor import HarvestingProcessor


def initialize_simulation(configuration):
    simulation_id = str(uuid.uuid4())

    blobs_on_field = {(i, j): [] for i in range(configuration['field_size']) for j in
                      range(configuration['field_size'])}

    blobs = {}

    for i in range(100):
        blob = {}
        blob['id'] = i
        blob['vitality'] = round(clamp(np.random.normal(configuration['vitality'], configuration['sd']), 1, 100))
        blob['charisma'] = round(clamp(np.random.normal(configuration['charisma'], configuration['sd']), 1, 100))
        blob['life'] = 100
        blob['speed'] = round((blob['life'] + blob['vitality']) / 40)
        blob['freeze'] = 0
        blob['location'] = random.randint(0, 99), random.randint(0, 99)
        blobs_on_field[blob['location']].append(i)
        blobs[i] = blob

    field = {(i, j): 0 for i in range(configuration['field_size'])
             for j in range(configuration['field_size'])}

    save_configuration(simulation_id, configuration)
    save_snapshot(simulation_id, 0, blobs, field, blobs_on_field)

    return simulation_id


def run_simulation(simulation_id, step):
    snapshot = get_snapshot_by_step(simulation_id, step)
    step, blobs, field, blobs_on_field = restore_snapshot(snapshot)

    configuration = get_config(simulation_id)

    for i in range(1, 101):
        if not (i % 24):
            FieldProcessor.exp(field)
            field.update(FieldProcessor.grow_food(field, configuration))
        HealthSpeedProcessor.process(blobs, blobs_on_field, configuration)
        MatingProcessor.process(blobs, blobs_on_field, configuration)
        HarvestingProcessor.process(field, blobs, blobs_on_field, configuration)
        save_snapshot(simulation_id, step + i, blobs, field, blobs_on_field)
