import os, re
from lib import db, constants

ABC_PATH = '../db/abc'
KEY_REGEX = "([{keys}]):(.+)".format(keys=''.join(constants.KEY_REFERENCE.keys()))


abc_files = []
for file in os.listdir(os.path.abspath(ABC_PATH)):
    if file.endswith(".abc"):
        abc_files.append(os.path.join(os.path.abspath(ABC_PATH),file))

for file in abc_files:
    file_obj = open(file, 'r')
    file_lines = file_obj.readlines()
    keys_used = []
    values_used = []
    tune_text = ""
    for line in file_lines:
        if re.search(KEY_REGEX) is not None:
            key, value = re.findall(KEY_REGEX)
            keys_used.append(constants.KEY_REFERENCE[key])
            values_used.append(value)
        else:
            tune_text += line + "\n"
    keys_used.append(constants.KEY_REFERENCE("F"))
    values_used.append(file)
    keys_used.append("tune_text")
    values_used.append(tune_text)

    print(keys_used)
    print(values_used)
