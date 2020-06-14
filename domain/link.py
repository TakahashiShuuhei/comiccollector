from datetime import datetime

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


class LinkRepository:
    def save(self, link: Link):
        raise NotImplementedError

    def get_all(self, page_id: int):
        raise NotImplementedError
