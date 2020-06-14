from typing import List
from domain.monitored_page import MonitoredPage

class Comic:
    """
    漫画
    """
    def __init__(self, id: int, title: str, url: str, pages: List[MonitoredPage]):
        self.id = id    
        self.title = title
        self.url = url
        self.pages = pages

    def check(self):
        raise NotImplementedError

    def add_page(self, page):
        self.pages.append(page)


class ComicRepository:
    def save(comic: Comic):
        raise NotImplementedError

    def get(id: int) -> Comic:
        raise NotImplementedError