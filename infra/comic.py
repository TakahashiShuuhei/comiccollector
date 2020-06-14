from domain.comic import Comic, ComicRepository
from domain.monitored_page import MonitoredPage, CollectionType
import sqlite3
from typing import List

class SqliteComicRepository(ComicRepository):
    """
    create table 
        comics
        (id integer primary key autoincrement,
         title text,
         url text)
    """
    def __init__(self, connection):
        self.connection = connection

    def save(self, comic: Comic) -> Comic:
        cursor = self.connection.cursor()
        if comic.id:
            cursor.execute('''
                update 
                    comics
                set 
                    title=?, url=? 
                where 
                    id=?''', (comic.title, comic.url, comic.id))
        else:
            cursor.execute('''
                insert into comics
                  (title, url)
                values
                   (?, ?)''', (comic.title, comic.url))
            comic.id = cursor.lastrowid
        return comic

    def get_all(self) -> List[Comic]:
        cursor = self.connection.cursor()
        cursor.execute('''
            select
                id,
                title,
                url
            from
                comics''')
        
        def _to_comic(row):
            return Comic(row[0], row[1], row[2], [])
        
        comics = {row[0]: _to_comic(row) for row in cursor.fetchall()}
        comic_ids = comics.keys()
        cursor.execute(f'''
            select
                id,
                url,
                comic_id,
                pattern,
                type
            from
                monitored_pages
            where
                comic_id in ({",".join(["?"]*len(comic_ids))})
        ''', list(comic_ids))
        def _to_page(row):
            return MonitoredPage(row[0], 
                                 row[1], 
                                 row[3], 
                                 CollectionType.name_to_type(row[4]))
        for row in cursor.fetchall():
            comic_id = row[2]
            page = _to_page(row)
            comic = comics.get(comic_id)
            comic.pages.append(page)
        return list(comics.values())
