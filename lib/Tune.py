
class Tune(object):
    name = ''
    version = ''
    type = ''
    metric = ''
    unit = ''
    tune_abc = ''
    link = ''
    key = ''
    tune_norm = ''

    def __init__(self, source):
        pass

    def parse_abc(self, abc_text):
        pass

    def parse_json(self, abc_text):
        pass

    def normalize_tune(self):
        pass

    def change_meter_note(self, beat_str, base_note, conversion_note=16):
        pass

    def transpose(self, beat_str, base_key, conversion_key='Cmay'):
        pass

    def get_note_duration(self, beat_str):
        pass

