from os import path, listdir
import re
from progress.bar import Bar
import json
from sys import exit

DB_SCRIPTS = path.abspath(path.dirname(__file__))
TUNE_FILE_PATH = path.abspath(path.dirname(__file__)  + path.sep + '..' + path.sep + 'download')

def split_tunes(abc_file, dest_path='{}{}abc'.format(DB_SCRIPTS, path.sep)):
    tune_buffer = ''
    c = 1
    file_name = path.basename(abc_file).split('.')[0]
    with open(abc_file, 'r') as f:
        for line in f:
            if re.match('X\:',line) and len(tune_buffer) > 0:
                file_to_write = '{path}{sep}{filename}_{count}.abc'.format(path=dest_path,
                                                                       sep=path.sep,
                                                                       filename=file_name,
                                                                       count=c)
                fw = open(file_to_write, 'w+')
                fw.write(tune_buffer)
                fw.close()
                c += 1
                tune_buffer = ''

            tune_buffer += line
        file_to_write = '{path}{sep}{filename}_{count}.abc'.format(path=dest_path,
                                                               sep=path.sep,
                                                               filename=file_name,
                                                               count=c)
        fw = open(file_to_write, 'w+')
        fw.write(tune_buffer)
        fw.close()


def split_tune_files(src_path=TUNE_FILE_PATH,
                     dest_path='{}{}abc'.format(DB_SCRIPTS, path.sep)):
    files = [path.join(src_path, f) for f in listdir(src_path)
             if path.isfile(path.join(src_path, f))]

    bar = Bar('Splitting Tunes', max=len(files))
    for item in files:
        split_tunes(item, dest_path)
        bar.next()


def abc_to_json(src_file, dest_file):
    parsed_tune = {}
    tune_text = ''
    with open(src_file, 'r') as abc_file:
        for line in abc_file:
            if re.match('^\w\:\s.*\r\n$', line):
                try:
                    m = re.search('^(\w)\:\s(.*)\r\n$', line)
                    key = m.group(1)
                    value = m.group(2)
                except Exception:
                    print 'ERROR processing file: ' + src_file
                    exit()

                if re.match('X', key):
                    parsed_tune['version'] = int(value.strip())
                elif re.match('T', key):
                    parsed_tune['title'] = value.strip()
                elif re.match('S', key):
                    parsed_tune['link'] = value.strip()
                elif re.match('R', key):
                    parsed_tune['type'] = value.strip()
                elif re.match('M', key):
                    parsed_tune['meter'] = value.strip()
                elif re.match('L', key):
                    parsed_tune['unit'] = value.strip()
                elif re.match('K', key):
                    parsed_tune['key'] = value.strip()
            else:
                tune_text += line
        parsed_tune['tune'] = tune_text
        abc_file.close()
    fw = open(dest_file, 'w+')
    fw.write(json.dumps(parsed_tune))
    fw.close()


def convert_abc_files_to_json(src_path, dest_path):
    files = [path.join(src_path, f) for f in listdir(src_path)
            if path.isfile(path.join(src_path, f))]

    bar = Bar('Converting to JSON', max=len(files))
    c = 1
    for src_file in files:
        dest_file = path.join(dest_path, '{}.json'.format(str(c).zfill(5)))
        abc_to_json(src_file, dest_file)
        bar.next()
        c += 1


if __name__ == '__main__':
    split_tune_files('/home/lordnano/PycharmProjects/TuneDB/download',
                     '/home/lordnano/PycharmProjects/TuneDB/db/abc')
    convert_abc_files_to_json('/home/lordnano/PycharmProjects/TuneDB/db/abc',
                              '/home/lordnano/PycharmProjects/TuneDB/db/json')


