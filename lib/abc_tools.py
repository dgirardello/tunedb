import re
import json


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


def extract_first_note(notes):
    return re.findall('[\^|\=|\_]?[a|b|c|d|e|f|g|A|B|C|D|E|F|G][\,|\']?', notes)[0]


def convert_to_dsq(abc_text, base_note_value=8):
    note_mult = int(32/base_note_value)
    pos = 0
    return_str = ''
    note = ''
    duration = 0
    while pos < len(abc_text):
        if re.match('[a|b|c|d|e|f|g|\^|=|_]', abc_text[pos], flags=re.IGNORECASE):
            note = extract_first_note(abc_text[pos:])
            pos += len(note)
            duration = 1

        if pos < len(abc_text) and re.match('[\d|<|>|/]', abc_text[pos]):
            if abc_text[pos:pos+3] == '3/2':
                duration = 1.5
                pos += 3
            elif re.match('\d', abc_text[pos]):
                duration = int(abc_text[pos])
                pos += 1
            elif re.match('/', abc_text[pos]):
                if abc_text[pos:pos+2] == '/2':
                    duration = 0.5
                    pos += 2
                elif abc_text[pos:pos+2] == '/3':
                    duration = 1.5
                    pos += 2
                elif abc_text[pos:pos+2] == '/4' or abc_text[pos:pos + 2] == '//':
                    duration = 0.25
                    pos += 2
                else:
                    duration = 0.5
                    pos += 1
            elif re.match('>', abc_text[pos]):
                return_str += note * int(note_mult * 1.5)
                pos += 1
                if pos < len(abc_text):
                    note = extract_first_note(abc_text[pos:])
                    pos += len(note)
                    duration = 0.5
            elif re.match('<', abc_text[pos]):
                return_str += note * int(note_mult * 0.5)
                pos += 1
                if pos < len(abc_text):
                    note = extract_first_note(abc_text[pos:])
                    pos += len(note)
                    duration = 1.5

        if len(note) > 0 and duration > 0:
            return_str += note * int(note_mult * duration)
            note = ''
            duration = 0

    return return_str


def convert_to_scale(abc_text, base_key):
    if str(base_key).lower() in ['cmaj', 'amin', 'gmix', 'ddor']:
        ret_str = abc_text
    elif str(base_key).lower() in ['gmaj', 'emin', 'dmix', 'ador']:
        ret_str = sharp_to_natural(abc_text, 'F')
    elif str(base_key).lower() in ['dmaj', 'bmin', 'amix', 'edor']:
        ret_str = sharp_to_natural(abc_text, 'F')
        ret_str = sharp_to_natural(ret_str, 'C')
    elif str(base_key).lower() in ['amaj', 'f#min', 'emix', 'bdor']:
        ret_str = sharp_to_natural(abc_text, 'F')
        ret_str = sharp_to_natural(ret_str, 'C')
        ret_str = sharp_to_natural(ret_str, 'G')

    return ret_str


def sharp_to_natural(text, note):
    lc_note = str(note).lower()
    uc_note = str(note).upper()
    return str(text).replace(lc_note, '^' + lc_note).replace(uc_note, '^' + uc_note).replace('=^', '')


def flat_to_natural(text, note):
    lc_note = str(note).lower()
    uc_note = str(note).upper()
    return str(text).replace(lc_note, '_' + lc_note).replace(uc_note, '_' + uc_note).replace('=_', '')
