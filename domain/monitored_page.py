from bs4 import BeautifulSoup
import requests
from retrying import retry
from domain.link import Link, CollectionType
from typing import Set
import re

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
        return [target.attrs.get(attr) for target in targets if p.match(target.attrs.get(attr))]

    def check(self, link_repository) -> Set[Link]:
        found_links = self.collect()
        saved_links = [link.url for link in link_repository.get_all(self.id)]
        new_links = set(found_links) - set(saved_links)
        if new_links:
            new_links = {Link(self.id, l, self.type) for l in new_links}
            for link in new_links:
                link_repository.save(link)
        return new_links
