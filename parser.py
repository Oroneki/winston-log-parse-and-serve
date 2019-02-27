from argparser import args
from halo import Halo
import sys
import json
import pathlib
from models import LogEntry, db


def yield_json_logs_from_folder(folder: str):
    count = 0
    path = pathlib.Path(folder)
    for arq in path.iterdir():
        if not arq.suffix == '.json':
            continue
        with open(arq, encoding='utf-8', errors='ignore') as f:
            print(arq)
            for line in f.readlines():
                try:
                    js = json.loads(line)
                    count = count + 1
                    yield js
                except:
                    pass
                    break
    print()
    print(count, 'log entries.')


def parse_and_save_to_db(folder: str):
    entries = []
    for i, js in enumerate(yield_json_logs_from_folder(folder)):
        entryDict = {
            'w': js.get('w'),
            'l': js.get('l'),
            't': js.get('t'),
            'ctx': js.get('ctx'),
            'p': js.get('p'),
            'message': js.get('message'),
            'mhu': js.get('mhu'),
            'mht': js.get('mht'),
            'mrss': js.get('mrss'),
            'ct': js.get('ct'),
            'cl': js.get('cl'),
        }
        entries.append(entryDict)
        if i % 70 == 0:
            LogEntry.insert_many(entries).execute()
            entries = []


def patiently_parse_log_folder(folder: str):
    with Halo(text='Parsing...', spinner='dots'):
        parse_and_save_to_db(folder)
    LogEntry.raw('CREATE INDEX t_sort ON logentry (t);').execute()


if __name__ == "__main__":
    patiently_parse_log_folder(args.f)
