from logging import config
import logging

config.fileConfig('batchlog.conf')
logger = logging.getLogger(__name__)

import sqlite3
from usecases.update_check import update_check
from infra.comic import SqliteComicRepository
from infra.link import SqliteLinkRepository


DB_PATH = './hoge.db'

if __name__ == '__main__':
    connection = sqlite3.connect(DB_PATH)
    comic_repository = SqliteComicRepository(connection)
    link_repository = SqliteLinkRepository(connection)
    update_check(connection, comic_repository, link_repository)
