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
    level: str = TextField()
    timestamp = DateTimeField()
    thread: str = TextField()
    message: str = TextField()
    memory_rss: int = IntegerField()
    memory_heap_total: int = IntegerField()
    memory_heap_used: int = IntegerField()
    memory_external: int = IntegerField()
    cpu_user: int = IntegerField()
    cpu_system: int = IntegerField()
    ms: str = TextField()


db.connect()
db.create_tables([LogEntry])
