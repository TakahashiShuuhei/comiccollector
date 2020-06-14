from domain.link import Link, LinkRepository
import sqlite3

class SqliteLinkRepository(LinkRepository):
    """
    create table
        links
        (id integer primary key autoincrement,
         url text,
         page_id integer,
         created_at text,
         foreign key(page_id) references monitored_pages(id)))
    """

    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(path)
    
    def save(self, link: Link):
        cursor = self.connection.cursor()
        cursor.execute('''
            insert into links
                (url, page_id, created_at)
            values
                (?, ?, ?)''', (link.url, link.page_id, link.created_at.isoformat()))
        self.connection.commit()
        return link

    def get_all(self, page_id: int):
        cursor = self.connection.cursor()
        cursor.execute('''
            select
                id, url, page_id, created_at
            from
                links
            where
                page_id=?
            order by
                created_at desc''', (page_id))
        result = []
        for row in cursor.fetchall():
            link = Link(page_id, row[1], datetime.fromisoformat(row[3]))
            result.append(link)
        return result
