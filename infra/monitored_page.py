from domain.monitored_page import MonitoredPage
import sqlite3

class SqliteMonitoredPageRepository:
    """
    todo comic.py に置くべき
    create table
        monitored_pages
        (id integer primary key autoincrement,
         url text,
         comic_id integer,
         pattern text,
         type text,
         foreign key(comic_id) references comics(id))
    """

    def __init__(self, connection):
        self.connection = connection
    
    def save(self, comic_id: int, page: MonitoredPage):
        cursor = self.connection.cursor()
        if page.id:
            cursor.execute('''
                update
                    monitored_pages
                set
                    url=?, pattern=?, type=?
                where
                    id=?''', (page.url, page.pattern, page.type.get('name'), page.id))
        else:
            cursor.execute('''
                insert into monitored_pages
                    (url, comic_id, pattern, type)
                values
                    (?, ?, ?, ?)''', (page.url, comic_id, page.pattern, page.type.get('name')))
            page.id = cursor.lastrowid
        self.connection.commit()
        return page
