from datetime import datetime
import os
import requests

class CollectionType:
    IMAGE = { 'name': 'IMAGE', 'tag': 'img', 'attr': 'src'}
    LINK = { 'name': 'LINK', 'tag': 'a', 'attr': 'href'}

    @classmethod
    def name_to_type(cls, name):
        m = {
            t.get('name'): t for t in [cls.IMAGE, cls.LINK]
        }
        return m.get(name)

class Link:
    """

    """
    def __init__(self, id: int, page_id: int, url: str, type: CollectionType, created_at: datetime =None):
        self.id = id
        self.page_id = page_id
        self.url = url
        self.type = type
        self.created_at = created_at if created_at else datetime.now()

    def save_file(self, parent_dir):
        if self.type != CollectionType.IMAGE:
            return
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        ext = self.url.split('.')[-1]
        file_name = f'{self.page_id}__{self.id}.{ext}'
        file_path = os.path.join(parent_dir, file_name)
        response = requests.get(self.url)
        with open(file_path, 'wb') as f:
            f.write(response.content)

class LinkRepository:
    def save(self, link: Link):
        raise NotImplementedError

    def get_all(self, page_id: int):
        raise NotImplementedError
