from .processor import Processor


class HealthSpeedProcessor(Processor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def process(blobs, blobs_on_field, configuration):
        blobs_to_delete = []
        for blob_id in blobs:
            blob = blobs[blob_id]
            blob['life'] -= configuration.life_decrease
            if blob['life'] <= 0:
                blobs_to_delete.append(blob['id'])
                blobs_on_field[blob['location']].remove(blob['id'])
            else:
                blob['speed'] = round((blob['life'] + blob['vitality']) / 40)
        for blob_id in blobs_to_delete:
            del blobs[blob_id]

