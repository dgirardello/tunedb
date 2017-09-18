import os
import re
import json

NOTES = []

class Tune(object):
    name = ''
    version = ''
    type = ''
    metric = ''
    unit = ''
    tune_abc = ''
    link = ''
    key = ''
    lines = []
    has_gracenotes = False
    has_triplets = False

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
        tune = ''
        for line in abc_text:
            if re.match('^[A-Z]\:[\s]?.*$', line):
                key = re.search('^([A-Z])\:[\s]?.*$', line).group(1)
                value = re.search('^[A-Z]\:[\s]?(.*)$', line).group(1)
                if re.match('X', key):
                    self.version = int(str(value).strip())
                elif re.match('T', key):
                    self.name = str(value).strip()
                elif re.match('S', key):
                    self.link = str(value).strip()
                elif re.match('R', key):
                    self.type = str(value).strip()
                elif re.match('M', key):
                    self.metric = str(value).strip()
                elif re.match('L', key):
                    self.unit = str(value).strip()
                elif re.match('K', key):
                    self.key = str(value).strip()
            else:
                tune += line
        if re.match('\{\w*\}', tune):
            self.has_gracenotes = True
        if re.match('\(\d\s?\w', tune):
            self.has_triplets = True
        self.tune_abc = tune

    def parse_json_tune(self, abc_text):
        pass

    def normalize_tune(self):
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


def parse_lines(tune_text):
    return tune_text.split('\n')


def parse_beats(line):
    return filter(None, re.split('\||\|]|\|\||\[\||\|:|:\||::', line))

def parse_fragment(beat):
    return filter(None, re.split('\s', beat))


def convert_to_dsq(abc_text, base_note_value=8):
    note_mult = int(32/base_note_value)
    pos = 0
    return_str = ''
    note = ''
    while pos < len(abc_text):
        # Detect Note
        if str(abc_text[pos:]).startswith('[\^|\=|\_]?\w'):
            if re.match('[\^|\=|\_]', abc_text[pos]):
                note += abc_text[pos]
                pos += 1
            if re.match('[a|b|c|d|e|f|g|A|B|C|D|E|F|G]', abc_text[pos]):
                note += abc_text[pos]
                pos += 1
            if re.match('[\,|\']', abc_text[pos]):
                note += abc_text[pos]
                pos += 1
            if pos >= len(abc_text):
                return_str += note * note_mult
                break

        # Detect duration
        if str(abc_text[pos:]).startswith('[\d|\<|\>|\\]'):
            if


    return return_str

def extract_first_note(notes):
    return re.findall('[\^|\=|\_]?[a|b|c|d|e|f|g|A|B|C|D|E|F|G][\,|\']?', notes)[0]