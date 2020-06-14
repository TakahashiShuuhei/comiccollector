import sqlite3
import os
from infra.comic import SqliteComicRepository
from infra.link import SqliteLinkRepository
from domain.link import CollectionType
import requests


DB_PATH = './hoge.db'
IMG_DIR = './imgs'

def update_check():
    connection = sqlite3.connect(DB_PATH)
    comic_repository = SqliteComicRepository(connection)
    link_repository = SqliteLinkRepository(connection)

    result = []
    comics = comic_repository.get_all()
    for comic in comics:
        new_links = comic.check(link_repository)
        if new_links:
            result.append((comic, new_links))
    if result:
        save_images(result)
        notify(result)
    connection.commit()


def save_images(result):
    # TODO 多分ここに書くべきじゃない
    for comic, links in result:
        dir_path = os.path.join(IMG_DIR, comic.title)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        for link in links:
            if link.type != CollectionType.IMAGE:
                continue
            ext = link.url.split('.')[-1]
            file_path = f'{comic.title}/{link.page_id}__{link.id}.{ext}'
            file_path = os.path.join(IMG_DIR, file_path)
            response = requests.get(link.url)
            with open(file_path, 'wb') as f:
                f.write(response.content)

def notify(result):
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    body = _to_mail_body(result)
    message = Mail(from_email='uhiaha888@gmail.com',
                   to_emails='uhiaha888@gmail.com',
                   subject='更新があったよ',
                   plain_text_content=body)
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)

def _to_mail_body(result):
    body = ''
    for comic, links in result:
        body += f'{comic.title}: {comic.url}\n\n'
        for link in links:
            body += f'    {link.url}\n'
        body += '\n'
    return body


if __name__ == '__main__':
    update_check()
