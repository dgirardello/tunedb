import os
import re
import json
import abc_tools


class Tune(object):
    name = ''
    version = ''
    type = ''
    metric = ''
    unit = ''
    tune_abc = ''
    link = ''
    key = ''
    ornamentation = False

    def __init__(self, source):
        if os.path.isfile(source):
            with open(source, 'r') as f:
                file_name = os.path.basename(source)
                if file_name.endswith('abc'):
                    self.parse_abc_tune(f)
                elif file_name.endswith('json'):
                    self.parse_json_tune(f)
        elif isinstance(source, str):
            if abc_tools.is_abc_tune(source):
                self.parse_abc_tune(source)
            elif abc_tools.is_json_tune(source):
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
                self.tune_abc += line
        if len(re.findall('[\{\(\~]', tune)) > 0:
            self.has_ornamentation = True
        else:
            try:
                self.converted_tune = ''
                for line in abc_tools.parse_lines(self.tune_abc):
                    for beat in abc_tools.parse_beats(line):
                        for fragment in abc_tools.parse_fragment(beat):
                            converted_fragment = abc_tools.convert_to_dsq(fragment, base_note_value=int(self.unit[-1]))
                            self.converted_tune += abc_tools.convert_to_scale(converted_fragment, self.key) + ' '
            except Exception as e:
                print 'Error converting the tune: {} ({})'.format(self.name, str(self.version))

    def parse_json_tune(self, abc_text):
        pass
