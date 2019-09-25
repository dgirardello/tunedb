import os, re
from lib import db, constants

ABC_PATH = '../db/abc'
KEY_REGEX = "([{keys}]):(.+)".format(keys=''.join(constants.KEY_REFERENCE.keys()))
DB_TABLE = 'library'


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
        if line.find("|") >= 0:
            tune_text += str(line)
        elif re.match(KEY_REGEX, line) is not None:
            key, value = re.findall(KEY_REGEX, line.strip())[0]
            keys_used.append(constants.KEY_REFERENCE[key.strip()])
            values_used.append(value.strip())
    keys_used.append(constants.KEY_REFERENCE["F"])
    values_used.append(file)
    keys_used.append("tune_text")
    values_used.append(tune_text)

    id = db.query_db_insert(table=DB_TABLE, columns=keys_used, values=values_used)
    print(id)
