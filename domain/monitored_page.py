from bs4 import BeautifulSoup
import requests
from retrying import retry

class CollectionType:
    IMAGE = { 'name': 'IMAGE', 'tag': 'img', 'attr': 'src'}
    LINK = { 'name': 'LINK', 'tag': 'a', 'attr': 'href'}

    @classmethod
    def name_to_type(cls, name):
        m = {
            t.get('name'): t for t in [cls.IMAGE, cls.LINK]
        }
        return m.get(name)

class MonitoredPage:
    """
    監視対象ページ
    """
    def __init__(self, id: int, url: str, pattern: str, type: CollectionType):
        self.id = id    
        self.url = url
        self.pattern = pattern
        self.type = type
    
    @retry(stop_max_attemp_number=20)
    def collect(self):
        """
        urlで指定されたページ内のリンクから、
        リンク先がpatternで指定された正規表現にマッチする画像URL/リンク先一覧を返す
        """
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tag = self.type['tag']
        targets = soup.find_all(tag)
        p = re.compile(pattern)
        attr = self.type['attr']
        return [target.attrs.get(attr) for target in targets if p.match(target.attrs.get(attr))]

    def check(self, link_repository):
        found_links = self.collect()
        saved_links = link_repository.get_all(self.id)
        new_links = set(found_links) - set(saved_links)
        if new_links:
            link_repository.save_links(self.id, new_links)
        return new_links
