from copy import copy


DEFAULT_CONFIGURATION = {
        'field_size': 100,
        'exp': 3,
        'sd': 1,
        'field_fertility': 5,
        'vitality': 50,
        'charisma': 50,
        'life_decrease': 1,
        'life_increase': 20,
        'prob_decrease': 0.2,
    }


def configure(parameters):
    configuration = copy(DEFAULT_CONFIGURATION)
    configuration.update(parameters)
    return configuration

