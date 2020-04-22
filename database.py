from peewee import SqliteDatabase, Model
from peewee import CharField, PrimaryKeyField, TimestampField
from pathlib import Path
from config import database_file


db = SqliteDatabase(Path.cwd() / database_file)


class BaseModel(Model):
    class Meta:
        database = db


class Topic(BaseModel):
    id = PrimaryKeyField(null=False)
    title = CharField()
    link = CharField()
    saved_on = TimestampField()
    announced_on = TimestampField()

    class Meta:
        db_table = 'topics'


db.connect()
if not Topic.table_exists():
    Topic.create_table()