from domain.comic import Comic, ComicRepository
import sqlite3

class SqliteComicRepository(ComicRepository):
    """
    create table 
        comics
        (id integer primary key autoincrement,
         title text,
         url text)
    """
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(path)

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
        self.connection.commit()
        return comic
