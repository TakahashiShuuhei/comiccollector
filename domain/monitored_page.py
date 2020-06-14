from bs4 import BeautifulSoup
import requests
from retrying import retry

class CollectionType:
    IMAGE = { 'tag': 'img', 'attr': 'src'}
    LINK = { 'tag': 'a', 'attr': 'href'}

class MonitoredPage:
    """
    監視対象ページ
    """
    def __init__(self, url: str, pattern: str, type: CollectionType):
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
