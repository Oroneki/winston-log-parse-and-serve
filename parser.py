import json
import pathlib
from models import LogEntry, db
from halo import Halo
from argparser import args


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
            'level': js['level'],
            'message': js['message'],
            'thread': js['thread'],
            'memory_rss': js['memory']['rss'],
            'memory_heap_total': js['memory']['heapTotal'],
            'memory_heap_used': js['memory']['heapUsed'],
            'memory_external': js['memory']['external'],
            'cpu_user': js['cpu']['user'],
            'cpu_system': js['cpu']['system'],
            'timestamp': js['timestamp'],
            'ms': js['ms'],
        }
        entries.append(entryDict)
        if i % 70 == 0:
            LogEntry.insert_many(entries).execute()
            entries = []


def patiently_parse_log_folder(folder: str):
    with Halo(text='Parsing...', spinner='dots'):
        parse_and_save_to_db(folder)


if __name__ == "__main__":
    patiently_parse_log_folder(args.f)
