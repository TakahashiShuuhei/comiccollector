from bs4 import BeautifulSoup
import requests
from retrying import retry
from domain.link import Link, CollectionType
from typing import List
import re
from urllib.parse import urlparse

class MonitoredPage:
    """
    監視対象ページ
    """
    def __init__(self, id: int, url: str, pattern: str, type: CollectionType):
        self.id = id    
        self.url = url
        self.pattern = pattern
        self.type = type
    
    @retry(stop_max_attempt_number=20)
    def collect(self):
        """
        urlで指定されたページ内のリンクから、
        リンク先がpatternで指定された正規表現にマッチする画像URL/リンク先一覧を返す
        """
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tag = self.type['tag']
        targets = soup.find_all(tag)
        p = re.compile(self.pattern)
        attr = self.type['attr']
        return [self._convert_link(target.attrs.get(attr)) for target in targets if p.match(target.attrs.get(attr))]

    def check(self, link_repository) -> List[Link]:
        found_links = self.collect()
        saved_links = [self._convert_link(link.url) for link in link_repository.get_all(self.id)]
        new_links = list(set(found_links) - set(saved_links))
        if new_links:
            new_links = [Link(None, self.id, l, self.type) for l in new_links]
            new_links.sort(key=lambda l: l.url)
            for link in new_links:
                link_repository.save(link)
        return new_links
    
    def _convert_link(self, link):
        if link.startswith('http'):
            return link
        url = self.url
        if url.endswith('/'):
            return url + link
        return url[:url.rfind('/')] + '/' + link

        
