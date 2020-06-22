from typing import List
from domain.page import Page
from domain.link import LinkRepository, Link
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)

class Comic:
    """
    漫画
    """
    def __init__(self, id: int, title: str, url: str, pages: List[Page]):
        self.id = id    
        self.title = title
        self.url = url
        self.pages = pages

    def check(self, link_repository: LinkRepository):
        logger.info(f'[{self.title}]の更新を確認します')
        new_links: List[Link] = []
        for page in self.pages:
            new_links.extend(page.check(link_repository, self.title))
        if new_links:
            logger.info(f'[{self.title}]で新しいリンクが{len(new_links)}見つかりました')
        else:
            logger.info(f'[{self.title}]で新しいリンクが見つかりませんでした')
        return new_links

    def add_page(self, page):
        self.pages.append(page)
    
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'pages': [p.to_json() for p in self.pages]
        }


class ComicRepository:
    def save(self, comic: Comic):
        raise NotImplementedError

    def get(self, id: int) -> Comic:
        raise NotImplementedError

    def get_all(self) -> List[Comic]:
        raise NotImplementedError
