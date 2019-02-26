from peewee import SqliteDatabase, Model, TextField, IntegerField, DateTimeField
import datetime
import os
from argparser import args

db = SqliteDatabase(args.db, pragmas={
    'journal_mode': 'wal',  # WAL-mode.
    'cache_size': -64 * 1000,  # 128MB cache.
    'synchronous': 0})  # Let the OS manage syncing.)


class BaseModel(Model):
    class Meta:
        database = db


class LogEntry(BaseModel):
    w: int = IntegerField()
    l: str = TextField()
    t: str = TextField()
    cxt: str = TextField(null=True)
    p: str = TextField(null=True)
    message: str = TextField()
    mhu: int = IntegerField()
    mht: int = IntegerField()
    mrss: int = IntegerField()
    ct: int = IntegerField()
    cl: int = IntegerField()

    def to_json(self):
        dic = self.__dict__['__data__']
        return dic


# class LogEntry(BaseModel):
#     level: str = TextField()
#     timestamp = DateTimeField()
#     thread: str = TextField()
#     message: str = TextField()
#     memory_rss: int = IntegerField()
#     memory_heap_total: int = IntegerField()
#     memory_heap_used: int = IntegerField()
#     memory_external: int = IntegerField()
#     cpu_user: int = IntegerField()
#     cpu_system: int = IntegerField()
#     ms: str = TextField()

#     def to_json(self):
#         dic = self.__dict__['__data__']
#         dic['timestamp'] = dic['timestamp'].isoformat()
#         return dic


db.connect()
db.create_tables([LogEntry])
