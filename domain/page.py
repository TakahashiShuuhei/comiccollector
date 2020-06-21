from bs4 import BeautifulSoup
import requests
from retrying import retry
from domain.link import Link, CollectionType
from enum import Enum, auto
from typing import List
import re
import os
from urllib.parse import urlparse


IMG_DIR = './imgs'

class PageType(Enum):
    LINK = auto()
    IMAGE = auto()
    PARENT = auto()


class Page:
    """
    監視対象ページ
    """
    def __init__(self, id: int, url: str, type: PageType):
        self.id = id    
        self.url = url
        self.type = type
    
    def collect(self):
        """
        urlで指定されたページ内のリンクから、監視対象のリンク先一覧を返す
        """
        raise NotImplementedError

    def check(self, link_repository, comic_title) -> List[Link]:
        """
        更新が検知されたリンク一覧を返す
        """
        raise NotImplementedError

    def _convert_link(self, link):
        if link.startswith('http'):
            return link
        url = self.url
        if url.endswith('/'):
            return url + link
        return url[:url.rfind('/')] + '/' + link

        
class LinkPage(Page):
    """
    リンクの追加を監視するページ
    """
    def __init__(self, id:int, url:str, pattern:str, tag:str = 'a', attr:str = 'href'):
        super(LinkPage, self).__init__(id, url, PageType.LINK)
        self.pattern = pattern
        self.tag = tag
        self.attr = attr
    
    @retry(stop_max_attempt_number=20)
    def collect(self):
        """
        urlで指定されたページ内のリンクから、
        リンク先がpatternで指定された正規表現にマッチするリンク先一覧を返す
        """
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tag = self.tag
        targets = soup.find_all(tag)
        p = re.compile(self.pattern)
        attr = self.attr
        return [self._convert_link(target.attrs.get(attr)) for target in targets if p.match(target.attrs.get(attr))]

    def check(self, link_repository, comic_title) -> List[Link]:
        collection_type = CollectionType.LINK

        found_links = self.collect()
        saved_links = [self._convert_link(link.url) for link in link_repository.get_all(self.id)]
        new_links = list(set(found_links) - set(saved_links))
        file_dir = os.path.join(IMG_DIR, comic_title)
        if new_links:
            new_links = [Link(None, self.id, l, collection_type) for l in new_links]
            new_links.sort(key=lambda l: l.url)
            for link in new_links:
                link_repository.save(link)
                link.save_file(file_dir)
        
        return new_links

class ImagePage(Page):
    """
    画像の追加を監視するページ
    """
    def __init__(self, id:int, url:str, pattern:str, tag:str = 'img', attr:str = 'src'):
        super(ImagePage, self).__init__(id, url, PageType.IMAGE)
        self.pattern = pattern
        self.tag = tag
        self.attr = attr

    @retry(stop_max_attempt_number=20)
    def collect(self):
        """
        urlで指定されたページ内のリンクから、
        リンク先がpatternで指定された正規表現にマッチする画像のリンク一覧を返す
        """
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tag = self.tag
        targets = soup.find_all(tag)
        p = re.compile(self.pattern)
        attr = self.attr
        return [self._convert_link(target.attrs.get(attr)) for target in targets if p.match(target.attrs.get(attr))]

    def check(self, link_repository, comic_title) -> List[Link]:
        collection_type = CollectionType.IMAGE

        found_links = self.collect()
        saved_links = [self._convert_link(link.url) for link in link_repository.get_all(self.id)]
        new_links = list(set(found_links) - set(saved_links))
        file_dir = os.path.join(IMG_DIR, comic_title)
        if new_links:
            new_links = [Link(None, self.id, l, collection_type) for l in new_links]
            new_links.sort(key=lambda l: l.url)
            for link in new_links:
                link_repository.save(link)
                link.save_file(file_dir)
        
        return new_links