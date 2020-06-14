from domain.monitored_page import MonitoredPage
from datetime import datetime

class Link:
    """

    """
    def __init__(self, page_id: int, url: str, type: MonitoredPage, created_at=None: datetime):
        self.page_id = page_id
        self.url = url
        self.type = type
        self.created_at = created_at if created_at or datatime.now()


class LinkRepository:
    def save(self, link: Link):
        raise NotImplementedError

    def get_all(self, page_id: int):
        raise NotImplementedError
