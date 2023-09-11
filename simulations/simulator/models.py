from mongoengine import *


class Blob(EmbeddedDocument):
    id = IntField(primary_key=True)
    vitality = IntField()
    charisma = IntField()
    life = IntField()
    speed = IntField()
    freeze = IntField()
    location = ListField()


class Snapshot(Document):
    simulation_id = StringField()
    step = IntField()
    blobs = DictField(EmbeddedDocumentField(Blob))
    field = DictField()
    blobs_on_field = DictField()

class Configuration(Document):
    simulation_id = StringField()
    field_size = IntField()
    exp = IntField()
    sd = IntField()
    field_fertility = IntField()
    vitality = IntField()
    charisma = IntField()
    life_decrease = IntField()
    life_increase = IntField()
    prob_decrease = FloatField()


class UserProfile(Document):
    user = IntField()
    simulations = ListField()

class NameSimulation(Document):
    simulation_id = StringField()
    name = StringField()
