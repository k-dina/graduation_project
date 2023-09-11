from .processor import Processor
from .functions import LOOK_AROUND, crop_area, get_vision_field, clamp
import numpy as np


class MatingProcessor(Processor):
    look_around = LOOK_AROUND

    def __init__(self):
        super().__init__()
        # self.__sd = configuration['sd']
        # self.__prob_decrease = configuration['prob_decrease']

    # self.__field_size = configuration['field_size']

    @staticmethod
    def process(blobs, blobs_on_field, configuration):

        pairs = MatingProcessor.__collect_pairs(blobs, blobs_on_field, configuration)

        for pair in pairs:
            pairs[pair] = MatingProcessor.__success_prob(blobs[pair[0]], blobs[pair[1]], configuration)

        pairs = MatingProcessor.__match_blobs(pairs)

        for pair in pairs:
            MatingProcessor.__new_blob(blobs[pair[0][0]], blobs[pair[0][1]], blobs, blobs_on_field, configuration)

    @staticmethod
    def __collect_pairs(blobs, blobs_on_field, configuration):
        pairs = {}

        for blob in blobs.values():

            if blob['life'] > 70 and not blob['freeze']:

                for location in crop_area(get_vision_field(blob['location'], MatingProcessor.look_around),
                                          configuration['field_size']):
                    if blobs_on_field[location]:
                        for other_blob in blobs_on_field[location]:
                            pair = tuple(sorted([blob['id'], other_blob]))
                            pairs[pair] = 0
        return pairs

    @staticmethod
    def __match_blobs(pairs):
        pairs = sorted([[key, value] for key, value in pairs.items()], key=lambda x: x[1], reverse=True)
        matched_blobs = set()

        for pair in pairs:
            if set(pair[0]) & matched_blobs:
                pair[1] = 0
            else:
                matched_blobs = matched_blobs | set(pair[0])

        pairs = filter(lambda x: x[1], pairs)
        return pairs

    @staticmethod
    def __new_blob(blob, other_blob, blobs, blobs_on_field, configuration):
        i = len(blobs)

        new_blob = {}
        new_blob['id'] = i

        mean = (blob['vitality'] + other_blob['vitality']) / 2
        sd = configuration['sd']
        new_blob['vitality'] = clamp(np.random.normal(mean, sd), 1, 100)

        mean = (blob['charisma'] + other_blob['charisma']) / 2
        new_blob['charisma'] = clamp(np.random.normal(mean, sd), 1, 100)

        new_blob['life'] = 100
        new_blob['speed'] = round((new_blob['life'] + new_blob['vitality']) / 40)
        new_blob['freeze'] = 3

        new_blob['location'] = blob['location']
        blobs_on_field[new_blob['location']].append(new_blob['id'])

        blobs[i] = new_blob

        blob['freeze'] = 3
        other_blob['freeze'] = 3

        return new_blob

    @staticmethod
    def __success_prob(blob, other_blob, configuration):
        distance = abs((other_blob['vitality'] - blob['vitality']) / 100)
        return 1 - distance - configuration['prob_decrease']
