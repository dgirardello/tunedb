
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

    def transpose_to_C(self, beat_str, base_key):
        # https://method-behind-the-music.com/theory/scalesandkeys/#transposition
        pass

    def get_note_duration(self, beat_str):
        # http://abcnotation.com/wiki/abc:standard:v2.2#note_lengths
        pass

