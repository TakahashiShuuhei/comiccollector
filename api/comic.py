import json

from api import app, get_db
from infra.comic import SqliteComicRepository
from usecases.list_comics import list_comics as u_list_comics
from flask import jsonify


@app.route('/')
def list_comics():
    comic_repo = SqliteComicRepository(get_db())
    comics = u_list_comics(comic_repo)
    return jsonify([c.to_json() for c in comics])
