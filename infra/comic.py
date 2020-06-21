from domain.comic import Comic, ComicRepository
from domain.page import Page, CollectionType, PageType, ImagePage, LinkPage, ParentPage
import json
import sqlite3
from typing import List

_page_types = {
    PageType.IMAGE.name: ImagePage,
    PageType.LINK.name: LinkPage,
    PageType.PARENT.name: ParentPage
}

class SqliteComicRepository(ComicRepository):
    """
    create table 
        comics
        (id integer primary key autoincrement,
         title text,
         url text);
    
    create table
        pages
        (id integer primary key autoincrement,
         url text,
         comic_id int,
         type text,
         attributes json,
         foreign key(comic_id) references comics(id));
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
                type,
                attributes
            from
                pages
            where
                comic_id in ({",".join(["?"]*len(comic_ids))})
        ''', list(comic_ids))

        def _to_page(row):
            page_type = row[3]
            clazz = _page_types.get(page_type)
            attributes = json.loads(row[4], strict=False)
            return clazz(row[0], row[1], **attributes)

        for row in cursor.fetchall():
            comic_id = row[2]
            page = _to_page(row)
            comic = comics.get(comic_id)
            comic.add_page(page)
        return list(comics.values())
