from typing import List
from domain.monitored_page import MonitoredPage
from domain.link import LinkRepository, Link
from dataclasses import dataclass


class Comic:
    """
    漫画
    """
    def __init__(self, id: int, title: str, url: str, pages: List[MonitoredPage]):
        self.id = id    
        self.title = title
        self.url = url
        self.pages = pages

    def check(self, link_repository: LinkRepository):
        new_links: List[Link] = []
        for page in self.pages:
            new_links.extend(page.check(link_repository))
        return new_links

    def add_page(self, page):
        self.pages.append(page)


class ComicRepository:
    def save(self, comic: Comic):
        raise NotImplementedError

    def get(self, id: int) -> Comic:
        raise NotImplementedError

    def get_all(self) -> List[Comic]:
        raise NotImplementedError
