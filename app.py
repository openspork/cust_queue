from flask import Flask
from peewee import SqliteDatabase

app = Flask(__name__)

#dictionary of locations to queues
queues = {}

#define database
db = SqliteDatabase('database.db')
