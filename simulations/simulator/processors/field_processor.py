from .processor import Processor
from .functions import clamp
import random


class FieldProcessor(Processor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def grow_food(field, configuration):
        empty_cells = list(filter(lambda x: field[x] == 0, field.keys()))

        food_amount = clamp(round(0.04 * configuration.field_size * configuration.field_size * configuration.field_fertility), 0,
                            len(empty_cells))
        new_food = random.sample(list(empty_cells), food_amount)

        return {x: configuration['exp'] for x in new_food}

    @staticmethod
    def exp(field):
        for key in field:
            if field[key] > 0:
                field[key] -= 1
