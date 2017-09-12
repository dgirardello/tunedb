import os
import re
import json
import music21

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
        if os.path.isfile(source):
            with open(source, 'r') as f:
                file_name = os.path.basename(source)
                if file_name.endswith('abc'):
                    self.parse_abc_tune(f)
                elif file_name.endswith('json'):
                    self.parse_json_tune(f)
        elif isinstance(source, str):
            if is_abc_tune(source):
                self.parse_abc_tune(source)
            elif is_json_tune(source):
                self.parse_json_tune(source)

    def parse_abc_tune(self, abc_text):
        pass

    def parse_json_tune(self, abc_text):
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


def is_abc_tune(tune_str):
    if not re.match('T\:[\s]]?.*', tune_str): return False
    if not re.match('R\:[\s]]?\w*', tune_str): return False
    if not re.match('M\:[\s]]?\d\\\d', tune_str): return False
    if not re.match('L\:[\s]]?\d\\\d', tune_str): return False
    if not re.match('K\:[\s]]?\w*', tune_str): return False
    if not re.match('\|.*\|', tune_str): return False
    return True


def is_json_tune(tune_str):
    try:
        loaded_tune = json.loads(tune_str)
    except ValueError:
        return False
    if not 'name' in loaded_tune: return False
    if not 'type' in loaded_tune: return False
    if not 'metric' in loaded_tune: return False
    if not 'unit' in loaded_tune: return False
    if not 'key' in loaded_tune: return False
    if not 'tune_abc' in loaded_tune: return False
    return True

