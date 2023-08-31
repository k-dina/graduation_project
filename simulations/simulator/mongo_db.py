import logging

import pymongo
from mongoengine import connect
from .models import Blob, Snapshot, Configuration

client = pymongo.MongoClient()

db = client['simulations']


connect('simulations', host='mongo', port=27017)

#Snapshot.create_index([('simulation_id', 1), ('step', 1)], unique=True)
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

def save_snapshot(id, step, blobs, field, blobs_on_field):
    blob_documents = {}
    for i in blobs:
        blob = Blob(**blobs[i])
        blob_documents[str(i)] = blob

    field = {str(key): value for key, value in field.items()}
    blobs_on_field = {str(key): value for key, value in blobs_on_field.items()}

    snapshot = Snapshot(simulation_id=id, step=step, blobs=blob_documents, field=field, blobs_on_field=blobs_on_field)
    logging.debug(snapshot)
    snapshot.save()


def save_configuration(id, configuration):
    configuration_doc = Configuration(**configuration)
    configuration_doc.simulation_id = id
    configuration_doc.save()


def get_snapshot_by_step(id, step):
    return Snapshot.objects.get(simulation_id=id, step=step)


def restore_snapshot(snapshot_document):
    step = snapshot_document.step
    blobs = {}  # Здесь будут восстановлены объекты blob

    for blob_id, blob_data in snapshot_document.blobs.items():
        blob = {
            'id': int(blob_data.id),
            'vitality': blob_data.vitality,
            'charisma': blob_data.charisma,
            'life': blob_data.life,
            'speed': blob_data.speed,
            'freeze': blob_data.freeze,
            'location': tuple(blob_data.location),  # Преобразуем список в кортеж
        }
        blobs[int(blob_id)] = blob

    field = {tuple(map(int, key.strip('()').split(', '))): value for key, value in snapshot_document.field.items()}
    blobs_on_field = {}
    for location_str, blob_list in snapshot_document.blobs_on_field.items():
        location = tuple(map(int, location_str.strip('()').split(', ')))  # Преобразуем строку в кортеж
        blobs_on_field[location] = blob_list

    return step, blobs, field, blobs_on_field


def get_config(id):
    return Configuration.objects.get(simulation_id=id)
