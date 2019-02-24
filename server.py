from flask import Flask, request, json
import enum
from peewee import Desc
from models import LogEntry
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)


class Level(enum.Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARN = 'warn'


class Worker(enum.Enum):
    MAIN = '_main_'
    T1 = '_th__1_'
    T2 = '_th__2_'
    T3 = '_th__3_'


def get_database(page: int = 1, level: Level = None, worker: Worker = None):
    print("page: ", page, "level: ", level, "worker: ", worker)
    number_of_records = 200
    query = LogEntry.select().order_by(
        Desc(LogEntry.timestamp)).paginate(page, number_of_records)
    if (not level is None) and (not worker is None):
        print("------------------------")
        query = LogEntry.select().where(
            (LogEntry.level == level), (LogEntry.thread == worker)
        ).order_by(
            Desc(LogEntry.timestamp)).paginate(page, number_of_records)
    if (level is None) and (not worker is None):
        print("------------------------")
        query = LogEntry.select().where(
            (LogEntry.thread == worker)
        ).order_by(
            Desc(LogEntry.timestamp)).paginate(page, number_of_records)
    if (not level is None) and (worker is None):
        print("------------------------")
        query = LogEntry.select().where(
            (LogEntry.level == level)
        ).order_by(
            Desc(LogEntry.timestamp)).paginate(page, 20)

    return [i.to_json() for i in query]


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api")
def handle_api():
    page = int(request.args.get('page'))
    level = request.args.get('level')
    worker = request.args.get('worker')
    print('request page: ', page, '| worker: ', worker, '| level: ', level)
    res = get_database(page, level, worker)
    return json.dumps(res)


if __name__ == "__main__":
    app.run()
