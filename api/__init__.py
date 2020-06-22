from flask import Flask, g
import sqlite3

DB_PATH = './hoge.db'

app = Flask(__name__)
# TODO set secret key
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()


app.teardown_appcontext(close_db)

from api import comic
